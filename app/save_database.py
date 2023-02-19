from teste import get_historical_k_line
import database as db_c
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Tuple
import time
from datetime import datetime, timedelta


def save_to_db(pair, time_step, datetime_str, db_url= "sqlite:////home/app/data/demo1.db"):
    # pair = "EURBUSD"
    # time_step = "5m"
    engine = sqlalchemy.create_engine(db_url)
    k_lines, first_k_line, last_k_line = get_historical_k_line(pair, time_step, datetime_str)
    # print(first_k_line, last_k_line )
    

    def add_to_db(kl_b):
        kl_db = db_c.K_line_h(
            # kline_id = kl_b["kline_id"],
            pair = kl_b["pair"],
            time_step = kl_b["time_step"],
            open_time_ms= kl_b["open_time_ms"],
            open_price= kl_b["open_price"],
            high_prioce= kl_b["high_prioce"],
            low_price= kl_b["low_price"],
            close_price= kl_b["close_price"],
            volume= kl_b["volume"],
            close_time_ms= kl_b["close_time_ms"],
            asset_volume= kl_b["asset_volume"],
            number_trade= kl_b["number_trade"],
            taker_buy_base_vol= kl_b["taker_buy_base_vol"],
            takes_buy_queote_vol= kl_b["takes_buy_queote_vol"],
            ignore= kl_b["ignore"]
        )
        return kl_db

    ks_k_lines_db = list(map( add_to_db, k_lines))
    
    
    db_c.Base.metadata.create_all(engine)
    with Session(engine) as session:
        
        session.add_all(ks_k_lines_db)
        session.commit()


def get_first_last(pair, time_step, db_str="sqlite:////home/app/data/demo1.db") -> Tuple[db_c.K_line_h, db_c.K_line_h]:
    stmt = select(db_c.K_line_h
                  ).where(db_c.K_line_h.pair.in_([pair])
                          ).where(db_c.K_line_h.time_step.in_([time_step]))
    

    # stmt.order_by("open_time_ms desc")
    # pass
    engine = sqlalchemy.create_engine(db_str)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    
    k_lines = list(session.scalars(stmt))
    first = k_lines[0]
    last  = k_lines[-1]
    return (first, last)


def get_data_until_now(pair, time_step, db_str="sqlite:////home/app/data/demo1.db"):

    r_need_more_requisition = True
    while r_need_more_requisition:
        first, last = get_first_last(pair, time_step, db_str)

        # curr_time = round(time.time()*1000)
        ini_time_for_now = datetime.now() - timedelta(minutes = 6)
        curr_time = round(ini_time_for_now.timestamp() * 1000)

        print(last, curr_time)
        r_need_more_requisition = last.open_time_ms <= curr_time

        if r_need_more_requisition:
            save_to_db(pair, time_step, last.open_time_ms, db_str)







def test_1():
    """
    Getting data and save.
    """
    
    pair = "EURBUSD"
    time_step = "5m"
    engine = sqlalchemy.create_engine("sqlite:////home/app/data/demo1.db")
    k_lines, first_k_line, last_k_line = get_historical_k_line(pair, time_step)
    # print(first_k_line, last_k_line )
    

    def add_to_db(kl_b):
        kl_db = db_c.K_line_h(
            # kline_id = kl_b["kline_id"],
            pair = kl_b["pair"],
            time_step = kl_b["time_step"],
            open_time_ms= kl_b["open_time_ms"],
            open_price= kl_b["open_price"],
            high_prioce= kl_b["high_prioce"],
            low_price= kl_b["low_price"],
            close_price= kl_b["close_price"],
            volume= kl_b["volume"],
            close_time_ms= kl_b["close_time_ms"],
            asset_volume= kl_b["asset_volume"],
            number_trade= kl_b["number_trade"],
            taker_buy_base_vol= kl_b["taker_buy_base_vol"],
            takes_buy_queote_vol= kl_b["takes_buy_queote_vol"],
            ignore= kl_b["ignore"]
        )
        return kl_db

    ks_k_lines_db = list(map( add_to_db, k_lines))
    
    
    db_c.Base.metadata.create_all(engine)
    with Session(engine) as session:
        
        session.add_all(ks_k_lines_db)
        session.commit()



    # db_c.K_line()


def test_2():
    # selecionando o ultimo preco pegado
    # db_c.K_line
    stmt = select(db_c.K_line_h
                  ).where(db_c.K_line_h.pair.in_(["EURBUSD"])
                          ).where(db_c.K_line_h.time_step.in_(["5m"]))
    

    # stmt.order_by("open_time_ms desc")
    # pass
    engine = sqlalchemy.create_engine("sqlite:////home/app/data/demo1.db")
    session = Session(engine)
    
    k_lines = list(session.scalars(stmt))
    print(k_lines[0])
    print(k_lines[-1])
    # for user in session.scalars(stmt):
        # print(user)
    
    print(type(stmt))

def test_3():
    pair = "EURBUSD"
    time_step = "5m"
    get_data_until_now(pair, time_step)

if __name__ == "__main__":
    # test_1()

    # test_2()
    test_3()
