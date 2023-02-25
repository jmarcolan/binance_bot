import database as db_c

from sqlalchemy.orm import Session
from sqlalchemy import select
import sqlalchemy

import teste as bi_tra



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

def get_qnt_coin_user_and_save(count_id, symbol, db_url= "sqlite:////home/app/data/bot.db"):
    res = bi_tra.get_user_asset_qnt(symbol)

    res["count_id"] = count_id
    add_new_history(res, db_url)
    # pass

def test_1():
    create_user = {
        # "count_id"    Column(Integer(), auto_increment=True, primary_key=True)
        "api_key"    : "teste",
        "api_secret" : "teste",
        "name"       : "teste",
        "password"   : "teste"
    }
    create_new_account(create_user)
def test_2():
    get_qnt_coin_user_and_save(1, "EUR")
    get_qnt_coin_user_and_save(1, "BUSD")
    get_qnt_coin_user_and_save(1, "BRL")
    get_qnt_coin_user_and_save(1, "BNB")

if __name__ == "__main__":
    test_1()
    test_2()