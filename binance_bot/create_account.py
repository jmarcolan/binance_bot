import binance_bot.database as db_c

from sqlalchemy.orm import Session
from sqlalchemy import select
import sqlalchemy

import binance_bot.binance_router as bi_tra
from configparser import ConfigParser


# config_object = ConfigParser()
# config_object.read("config.ini")
# key_binance = config_object["keys"]

def get_account_and_client(acc_id, db_url= "sqlite:////home/app/data/bot.db"):
    stmt = select(db_c.Account).where(db_c.Account.count_id.in_([acc_id]))
    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    k_lines = list(session.scalars(stmt))
    session.close()
    user = k_lines[0]

    cliente = bi_tra.get_client_binance(user.api_key, user.api_secret)
    return user, cliente

def get_account_by_user(user, db_url= "sqlite:////home/app/data/bot.db"):
    stmt = select(db_c.Account).where(db_c.Account.name.in_([user]))
    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    k_lines = list(session.scalars(stmt))
    session.close()
    user = k_lines[0]
    return user

def create_new_account(dic_bot, db_url= "sqlite:////home/app/data/bot.db"):
    engine = sqlalchemy.create_engine(db_url)
    kl_db = db_c.Account(**dic_bot)
    db_c.Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([kl_db])
        session.commit()


def add_new_history(dic_bot, db_url= "sqlite:////home/app/data/bot.db"):
    engine = sqlalchemy.create_engine(db_url)
    kl_db = db_c.Bot_account_coin_history(**dic_bot)
    db_c.Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([kl_db])
        session.commit()

def get_qnt_coin_user_and_save(client, count_id, symbol, db_url= "sqlite:////home/app/data/bot.db"):
    
    res = bi_tra.get_user_asset_qnt(client, symbol)
    
    res["count_id"] = count_id
    add_new_history(res, db_url)
    # pass

def test_1():
    key_binance = {
        "api_key": "KDy5NfXf3Qfu8arKbluB7WoLFHqe5CT02D91LURPthunZApRMks4yC5XShgLs3A3",
        "api_secret": "1JHZxijq6SqeeKDlgMgPsf3Rn0Il3SW9jZiIGGADT83FnqSO91LCzsVqrHDPyXtT"
    }
    create_user = {
        # "count_id"    Column(Integer(), auto_increment=True, primary_key=True)
        "api_key"    : key_binance['api_key'],
        "api_secret" : key_binance['api_secret'],
        "name"       : "jmarcolan",
        "password"   : "teste"
    }
    create_new_account(create_user)

def getting_qnt_coins():
    user, client = get_account_and_client(1, db_url= "sqlite:////home/app/data/bot.db")
    get_qnt_coin_user_and_save(client, 1, "EUR")
    get_qnt_coin_user_and_save(client, 1, "BUSD")
    get_qnt_coin_user_and_save(client, 1, "BRL")
    get_qnt_coin_user_and_save(client, 1, "BNB")

if __name__ == "__main__":
    test_1()
    getting_qnt_coins()