from binance_bot.binance_router import get_transaction_satus

import binance_bot.database as db_c
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from typing import Tuple, List, Dict
import time
from datetime import datetime, timedelta
import json

import glob



def save_transaction(ls_dic_binance:List[Dict], db_url = "sqlite:////home/app/data/binance_transaction.db"):
    def create_db_tran(dic_binance:Dict):
        if dic_binance.get("fills", None) != None:
            del dic_binance["fills"]

        di = db_c.B_transaction(**dic_binance)
        return di
            
    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    
    ls_save = list(map(create_db_tran, ls_dic_binance))
    with Session(engine) as session:    
        session.add_all(ls_save)
        session.commit()


def test_create_db():
    def open_file_json(file_name):
        with open(file_name, "r") as file:
            txt = file.read()
        return json.loads(txt)
    
    ls_files = [name for name in glob.glob('./test_NEW_*.json')]
    ls_binance = list(map(open_file_json, ls_files))
    save_transaction(ls_binance)


def get_transaction_binance( id_transac, db_url):
    update_new_transaction(db_url)
    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    stmt = select(db_c.B_transaction).where(db_c.B_transaction.orderId == id_transac)
    t_open = list(session.scalars(stmt))
    if len(t_open) == 0:
        return None
    
    return t_open[0]


def update_new_transaction(client, db_url = "sqlite:////home/app/data/binance_transaction.db"):
    def create_db_tran(dic_binance:Dict):
        if dic_binance.get("fills", None) != None:
            del dic_binance["fills"]

        di = db_c.B_transaction(**dic_binance)
        return di

    def update_db(dic_upd): 
        engine = sqlalchemy.create_engine(db_url)
        db_c.Base.metadata.create_all(engine)
        session = Session(engine)
        od_id = dic_upd['orderId']
        del dic_upd['orderId']

        a = session.query(db_c.B_transaction).filter(
                        db_c.B_transaction.orderId ==od_id).update(
                        dic_upd, synchronize_session="fetch")
        
        session.commit()
        session.close()
        return a
    


    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    stmt = select(db_c.B_transaction
                  ).where(db_c.B_transaction.status.in_(["NEW"]))
    
    
    t_open = list(session.scalars(stmt))
    session.close()

    t_open_id = list(map(lambda x: (x.symbol, x.orderId) , t_open))
    t_updated = list(map(lambda x: get_transaction_satus(client, x[0], x[1]), t_open_id))

    ls_a = list(map(update_db, t_updated))
    print(len(t_open))

    # print(t_updated)

def create_new_transaction(ls_binance:List[Dict], db_url= "sqlite:////home/app/data/binance_transaction.db"):
    save_transaction(ls_binance, db_url)


if __name__ == "__main__":
    # update_new_transaction()
    transac_1 = get_transaction_binance(137622826, "sqlite:////home/app/data/binance_transaction.db")

    print(transac_1)