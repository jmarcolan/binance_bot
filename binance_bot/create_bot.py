import binance_bot.database as db_c
import sqlalchemy

from sqlalchemy.orm import Session
from sqlalchemy import select

import binance_bot.transaction_database as td
import binance_bot.binance_router as bi_tra
import binance_bot.create_account as acc
import copy

import time


def get_all_bot_activate(db_url= "sqlite:////home/app/data/bot.db"):
    stmt = select(db_c.Bot_info).where(
        db_c.Bot_info.status.in_(["ACTIVATED"])) 

    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    k_lines = list(session.scalars(stmt))
    session.close()
    return k_lines


def create_new_bot(dic_bot, db_url= "sqlite:////home/app/data/bot.db"):

    engine = sqlalchemy.create_engine(db_url)
    kl_db = db_c.Bot_info(**dic_bot)
    db_c.Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([kl_db])
        session.commit()

def create_new_trans(dic_tran, db_url= "sqlite:////home/app/data/bot.db"):

    engine = sqlalchemy.create_engine(db_url)
    kl_db = db_c.Bot_tran(**dic_tran)
    db_c.Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([kl_db])
        session.commit()

def get_list_transact_open(bot_id, value, db_url= "sqlite:////home/app/data/bot.db"):
    stmt = select(db_c.Bot_tran).where(
        db_c.Bot_tran.bot_id == bot_id).where(
        db_c.Bot_tran.sell_status.in_(["NEW", "WAIT", "FILLED"])).where(
        db_c.Bot_tran.buy_satus.in_(["NEW", "WAIT", "WAIT_SELL"])).where(
        db_c.Bot_tran.buy_price <= value).where(
        db_c.Bot_tran.sell_price > value)
    

    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    k_lines = list(session.scalars(stmt))
    session.close()
    return k_lines

def get_list_buy_incomplete(bot_id, value, sell=["FILLED"], buy= ["CANCELED"], db_url= "sqlite:////home/app/data/bot.db"):
    stmt = select(db_c.Bot_tran).where(
        db_c.Bot_tran.bot_id == bot_id).where(
        db_c.Bot_tran.sell_status.in_(sell)).where(
        db_c.Bot_tran.buy_satus.in_(buy)).where(
        db_c.Bot_tran.buy_price <= value).where(
        db_c.Bot_tran.sell_price > value)
    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    k_lines = list(session.scalars(stmt))
    session.close()
    return k_lines


def get_list_transact_open_buy(bot_id, value, db_url= "sqlite:////home/app/data/bot.db"):
    stmt = select(db_c.Bot_tran).where(
        db_c.Bot_tran.bot_id.in_([bot_id])).where(
        db_c.Bot_tran.sell_status.in_(["NEW", "WAIT", "WAIT_BUY"])).where(
        db_c.Bot_tran.buy_satus.in_(["NEW", "WAIT", "FILLED"])).where(
        db_c.Bot_tran.buy_price <= value).where(
        db_c.Bot_tran.sell_price > value)
    

    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    k_lines = list(session.scalars(stmt))
    session.close()
    return k_lines


def get_sell_buy_status(bot_id, sell_status= ["WAIT", "WAIT_BUY", "NEW", "FILLED", "CANCELED"], buy_status= ["WAIT", "WAIT_SELL", "NEW", "FILLED", "CANCELED"], db_url= "sqlite:////home/app/data/bot.db"):
    stmt = select(db_c.Bot_tran).where(
        db_c.Bot_tran.bot_id.in_([bot_id])).where(
        db_c.Bot_tran.sell_status.in_(sell_status)).where(
        db_c.Bot_tran.buy_satus.in_(buy_status)) 

    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    k_lines = list(session.scalars(stmt))
    session.close()
    return k_lines



def get_sell_status(bot_id, status= ["WAIT", "WAIT_BUY", "NEW", "FILLED", "CANCELED"], db_url= "sqlite:////home/app/data/bot.db"):
    stmt = select(db_c.Bot_tran).where(
        db_c.Bot_tran.bot_id.in_([bot_id])).where(
        db_c.Bot_tran.sell_status.in_(status)) 

    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    k_lines = list(session.scalars(stmt))
    session.close()
    return k_lines



def get_buy_status(bot_id, status= ["WAIT", "WAIT_BUY", "NEW", "FILLED", "CANCELED"], db_url= "sqlite:////home/app/data/bot.db"):
    stmt = select(db_c.Bot_tran).where(
        db_c.Bot_tran.bot_id.in_([bot_id])).where(
        db_c.Bot_tran.buy_satus.in_(status)) 

    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    k_lines = list(session.scalars(stmt))
    session.close()
    return k_lines

def update_bot_using_object(t_wait:db_c.Bot_tran, db_url):
    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    session.add(t_wait)
    session.commit()


def upate_bot_transact(t_wait:db_c.Bot_tran, db_url):
    def update_db(dic_upd): 
        engine = sqlalchemy.create_engine(db_url)
        db_c.Base.metadata.create_all(engine)
        session = Session(engine)
        od_id = dic_upd['ts_id']
        del dic_upd['ts_id']

        a = session.query(db_c.Bot_tran).filter(
                        db_c.Bot_tran.ts_id == od_id).update(
                        dic_upd, synchronize_session="fetch")
        
        session.commit()
        session.close()
        return a
    
    # response["orderId"]
    d_update = copy.deepcopy(t_wait.__dict__)
    r_exi = d_update.get("_sa_instance_state", None) != None
    if r_exi:
        del d_update["_sa_instance_state"]

    update_db(d_update)



    


def get_bot_inf_by_id(bot_id, db_url= "sqlite:////home/app/data/bot.db"):
    stmt = select(db_c.Bot_info).where(db_c.Bot_info.bot_id.in_([bot_id]))
    engine = sqlalchemy.create_engine(db_url)
    db_c.Base.metadata.create_all(engine)
    session = Session(engine)
    k_lines = list(session.scalars(stmt))
    session.close()
    return k_lines[0]



class BotGridDolar:
    def __init__(self, bot_id, db_url="sqlite:////home/app/data/bot.db") -> None:
        # pass
        self.db_url = db_url
        self.bot_info:db_c.Bot_info = get_bot_inf_by_id(bot_id)
        user, client = acc.get_account_and_client(self.bot_info.count_id, db_url= db_url)
        self.bot_id = self.bot_info.bot_id
        self.client = client


        # self.account_id = account_id
        self.delta_price = 0.001
        self._create_grid_bot(self.bot_info.delta_price, self.bot_info.bot_price, self.bot_info.top_price )
    
    def _create_grid_bot(self, delta_price, value_init, value_end):
        d_value = round((float(value_end) - float(value_init))/float(delta_price)) + 1
        delta_price_f = float(delta_price)
        value_init_f = float(value_init)
        bot_price = list(map(lambda x: round(x,3), map(lambda value :(value*delta_price_f + value_init_f),range(d_value))))
        top_price = list(map(lambda x: round(x,3), map(lambda value :(value*delta_price_f + value_init_f),range(1, d_value))))
        self.pair_step = list(zip(bot_price,top_price))
    
    def _check_if_has_transaction(self, bot_id, value_pair):
        ls_tra = get_list_transact_open(bot_id, value_pair, db_url=self.db_url)
        
        print(ls_tra)
        return len(ls_tra) > 0

    def _creat_new_transaction(self, top_price, bot_price,  bot_id,  symbol, quantity):
        dic_bot = {"symbol"      : symbol, 
                   "bot_id": bot_id,
                   "sell_price" : str(top_price),
                   "sell_status" : "WAIT",
                   "sell_qnt"   : str(quantity),
                   "buy_price"  : str(bot_price),
                   "buy_satus"  : "WAIT_SELL",
                   "buy_qnt"   : str(quantity)}
        create_new_trans(dic_bot, self.db_url)

    def _check_incomplete(self, bot_id, value_pair):
        ls_tra = get_list_buy_incomplete(bot_id, value_pair, sell=["FILLED"], buy= ["CANCELED"], db_url=self.db_url)
         ## reopen the operation
        # ls_tra[0] buy_satus : "WAIT"
        # upate_bot_transact(t_wait, self.db_url)
        for t_tra in ls_tra:
        # t_tra = ls_tra[0]
            # reviving 
            t_tra.buy_satus = "WAIT"
            update_bot_using_object(t_tra, self.db_url)
        # print(ls_tra)
        return len(ls_tra) > 0


    def new_transaction(self, value_pair):
        cur_step = list(filter( lambda x: x[0] <= value_pair and x[1] > value_pair, self.pair_step))
        r_out = len(cur_step) ==0 
        if r_out:
            print("its on the limiar or out of range")
            return False
        print("the current step", cur_step[0])
        cur_step = cur_step[0]
        
        t_transaction_incomplete= self._check_incomplete(self.bot_id, value_pair)
        if t_transaction_incomplete:
           
            return True

        t_transactio_open = self._check_if_has_transaction(self.bot_id, value_pair)
        print(t_transactio_open)
        if t_transactio_open:
            return False
        

        self._creat_new_transaction( cur_step[1], cur_step[0], self.bot_id, self.bot_info.symbol, self.bot_info.quantity )
        return True

class BotGridDolarBUY(BotGridDolar):
    def __init__(self, bot_id, db_url="sqlite:////home/app/data/bot.db") -> None:
        super().__init__(bot_id, db_url)
    
    def _check_if_has_transaction(self, bot_id, value_pair):
        ls_tra = get_list_transact_open_buy(bot_id, value_pair, db_url=self.db_url)
        print(ls_tra)
        return len(ls_tra) > 0
    def _check_incomplete(self, bot_id, value_pair):
        ls_tra = get_list_buy_incomplete(bot_id, value_pair, sell = ["CANCELED"], buy= ["FILLED"], db_url=self.db_url)
         ## reopen the operation
        # ls_tra[0] buy_satus : "WAIT"sell=["FILLED"], buy= ["CANCELED"]
        # upate_bot_transact(t_wait, self.db_url)
        for t_tra in ls_tra:
        # t_tra = ls_tra[0]
            # reviving 
            t_tra.sell_status = "WAIT"
            update_bot_using_object(t_tra, self.db_url)
        # print(ls_tra)
        return len(ls_tra) > 0
    def _creat_new_transaction(self, top_price, bot_price,  bot_id,  symbol, quantity):
        # isso é interessente para a operação de dolar gerar 
        # euros, mas as orderm são muito pequenas para praticar ainda
        # precisao da quantidade é 1 (ex. 11.9, 12.1) e não more (ex 11.93)
        # qnt_other = float(bot_price) * float(quantity) # eurdol, isso fica dol
        # qnt_sell  = round(qnt_other/ float(top_price),7)
        qnt_sell = quantity
        dic_bot = {"symbol"      : symbol, 
                   "bot_id": bot_id,
                   "sell_price" : str(top_price),
                   "sell_status" : "WAIT_BUY",
                   "sell_qnt"   : str(qnt_sell),
                   "buy_price"  : str(bot_price),
                   "buy_satus"  : "WAIT",
                   "buy_qnt"   : str(quantity)}
        create_new_trans(dic_bot, self.db_url)
        

class SincWithBinance:
    def __init__(self, db_url, bot_id) -> None:
        self.db_url = db_url
        self.bot_id = bot_id
        self.bot_info:db_c.Bot_info = get_bot_inf_by_id(bot_id)
        user, client = acc.get_account_and_client(self.bot_info.count_id, db_url=db_url)
        self.client = client
    
    def _update_transacition_binance(self):
        td.update_new_transaction(self.client, self.db_url)


    def _update_transaction_bot(self):
        def create_new_transaction_sell(t_wait:db_c.Bot_tran):
            print(t_wait)
            r_worked, response = bi_tra.create_new_order(self.client, t_wait.symbol, "SELL", round(float(t_wait.sell_qnt), 3), round(float(t_wait.sell_price), 3))
            if r_worked:
                td.create_new_transaction([response], self.db_url)
                t_wait.sell_id = response["orderId"]
                t_wait.sell_status = response["status"]
                upate_bot_transact(t_wait, self.db_url)

            return response

        def create_new_transaction_buy(t_filled:db_c.Bot_tran):
            r_worked, response = bi_tra.create_new_order(self.client, t_filled.symbol, "BUY", round(float(t_filled.buy_qnt), 3), round(float(t_filled.buy_price), 3))
            if r_worked:
                td.create_new_transaction([response], self.db_url)
                t_filled.buy_id = response["orderId"]
                t_filled.buy_satus = response["status"]
                upate_bot_transact(t_filled, self.db_url)

            return response
        
        def check_if_sell_filled(t_new:db_c.Bot_tran):
            orderId =  t_new.sell_id
            tran_binance = td.get_transaction_binance(orderId, self.db_url)
            if tran_binance == None:
                return False
            
            t_new.sell_status = tran_binance.status
            upate_bot_transact(t_new, self.db_url)
            # t_new.sell_price = tran_binance.price
            # t_new.sell_qnt   = tran_binance.

        def check_if_buy_filled(t_new:db_c.Bot_tran):
            orderId =  t_new.buy_id
            tran_binance = td.get_transaction_binance(orderId, self.db_url)
            if tran_binance == None:
                return False
            
            t_new.buy_satus = tran_binance.status
            upate_bot_transact(t_new, self.db_url)


        ls_transac = get_sell_status(self.bot_id, ["WAIT"] ,self.db_url)
        _ = list(map(create_new_transaction_sell, ls_transac))

        ls_transac = get_sell_status(self.bot_id, ["NEW"] ,self.db_url)
        _ = list(map(check_if_sell_filled, ls_transac))

        ls_transac = get_sell_buy_status(self.bot_id, ["FILLED"], ["WAIT", "WAIT_SELL"], self.db_url)
        _ = list(map(create_new_transaction_buy, ls_transac))

        ls_transac = get_buy_status(self.bot_id, ["NEW"] ,self.db_url)
        _ = list(map(check_if_buy_filled, ls_transac))
        

    def sinc_db_binance(self):
        self._update_transacition_binance()
        self._update_transaction_bot()


class SincWithBinanceBUY(SincWithBinance):
    def __init__(self, db_url, bot_id) -> None:
        super().__init__(db_url, bot_id)
    
    def _update_transaction_bot(self):
        def create_new_transaction_sell(t_wait:db_c.Bot_tran):
            print(t_wait)
            r_worked, response = bi_tra.create_new_order(self.client, t_wait.symbol, "SELL", float(t_wait.sell_qnt), float(t_wait.sell_price))
            if r_worked:
                td.create_new_transaction([response], self.db_url)
                t_wait.sell_id = response["orderId"]
                t_wait.sell_status = response["status"]
                upate_bot_transact(t_wait, self.db_url)

            return response

        def create_new_transaction_buy(t_filled:db_c.Bot_tran):
            r_worked, response = bi_tra.create_new_order(self.client, t_filled.symbol, "BUY", round(float(t_filled.buy_qnt), 3), round(float(t_filled.buy_price), 3))
            if r_worked:
                td.create_new_transaction([response], self.db_url)
                t_filled.buy_id = response["orderId"]
                t_filled.buy_satus = response["status"]
                upate_bot_transact(t_filled, self.db_url)

            return response
        
        def check_if_sell_filled(t_new:db_c.Bot_tran):
            orderId =  t_new.sell_id
            tran_binance = td.get_transaction_binance(orderId, self.db_url)
            if tran_binance == None:
                return False
            
            t_new.sell_status = tran_binance.status
            upate_bot_transact(t_new, self.db_url)
            # t_new.sell_price = tran_binance.price
            # t_new.sell_qnt   = tran_binance.

        def check_if_buy_filled(t_new:db_c.Bot_tran):
            orderId =  t_new.buy_id
            tran_binance = td.get_transaction_binance(orderId, self.db_url)
            if tran_binance == None:
                return False
            
            t_new.buy_satus = tran_binance.status
            upate_bot_transact(t_new, self.db_url)


        ls_transac = get_buy_status(self.bot_id, ["WAIT"] ,self.db_url)
        _ = list(map(create_new_transaction_buy, ls_transac))
        # get_buy_status
        # create_new_transaction_buy

        ls_transac = get_buy_status(self.bot_id, ["NEW"] ,self.db_url)
        _ = list(map(check_if_buy_filled, ls_transac))
        # get_buy_status
        # check_if_buy_filled

        ls_transac = get_sell_buy_status(self.bot_id, ["WAIT", "WAIT_BUY"], ["FILLED"], self.db_url)
        _ = list(map(create_new_transaction_sell, ls_transac))

        # get_sell_buy_status  ["WAIT", "WAIT_BUY"], ["FILLED"]
        # create_new_transaction_sell

        ls_transac = get_sell_status(self.bot_id, ["NEW"] ,self.db_url)
        _ = list(map(check_if_sell_filled, ls_transac))
        # get_sell_status
        # check_if_sell_filled
    

def test_update():
    def create_new_transaction(t_wait:db_c.Bot_tran):
            
        # r_worked, response = bi_tra.create_new_order(t_wait.symbol, "SELL", t_wait.sell_qnt, t_wait.sell_price )
        # if r_worked:
            # td.create_new_transaction([response], self.db_url)
            
        t_wait.sell_id = 123123 #response["orderId"]
        t_wait.sell_status = "NEW"
        upate_bot_transact(t_wait, db_url= "sqlite:////home/app/data/bot.db" )
        return True
        # return response
    ls_transac = get_sell_status(1, ["WAIT"])
    ls_tran = list(map(create_new_transaction, ls_transac))


def test_create_new_bot():
    # this bot first sell and second sell
    # so sell eur to busd an after  buy busd
    dic_bot = {"symbol"      : "EURBUSD",
        "status": "ACTIVATED",
        "delta_price" : "0.004",
        "bot_price"   : "0.8",
        "top_price"   : "1.2",
        "quantity"    : "11.9",
        "count_id": 1,
        "type_bot": "SELLBUY"
        }
    
    create_new_bot(dic_bot)

def test_create_new_bot_buy_sell():
    dic_bot = {"symbol"      : "EURBUSD",
        "status": "ACTIVATED",
        "delta_price" : "0.004",
        "bot_price"   : "0.802",
        "top_price"   : "1.2",
        "quantity"    : "11.9",
        "count_id": 1,
        "type_bot": "BUYSELL"
        }
    
    create_new_bot(dic_bot)
def keep_live():
    
    bot = BotGridDolar(1)
    sinc = SincWithBinance("sqlite:////home/app/data/bot.db", 1)

    user, client = acc.get_account_and_client(1, db_url= "sqlite:////home/app/data/bot.db")
    while True:
        price = bi_tra.get_current_price(client,bot.bot_info.symbol)
        print(price)
        bot.new_transaction(price)
        sinc.sinc_db_binance()
        time.sleep(10)


def test_get_all(db_url="sqlite:////home/app/data/bot.db"):
    ls_bot_act = get_all_bot_activate()
    for bot_activ in ls_bot_act:
        print(bot_activ)
        if (bot_activ.type_bot == "BUYSELL"):
            print("OPERATION BUYSELL")
            bot_id = bot_activ.bot_id
            acc_id = bot_activ.count_id
            bot = BotGridDolarBUY(bot_id)
            sinc = SincWithBinanceBUY(db_url, bot_id)
            user, client = acc.get_account_and_client(acc_id, db_url= db_url)
            price = bi_tra.get_current_price(client, bot.bot_info.symbol)
            print(price)
            bot.new_transaction(price)
            sinc.sinc_db_binance()
        
        elif(bot_activ.type_bot == "SELLBUY"):
            print("OPERATION SELLBUY")
            bot_id = bot_activ.bot_id
            acc_id = bot_activ.count_id
            bot = BotGridDolar(bot_id)
            sinc = SincWithBinance(db_url, bot_id)
            user, client = acc.get_account_and_client(acc_id, db_url= db_url)
            price = bi_tra.get_current_price(client, bot.bot_info.symbol)
            print(price)
            bot.new_transaction(price)
            sinc.sinc_db_binance()

def test_kepp_alive_buy_sell():
    bot = BotGridDolarBUY(1)
    sinc = SincWithBinanceBUY("sqlite:////home/app/data/bot.db", 1)

    user, client = acc.get_account_and_client(1, db_url= "sqlite:////home/app/data/bot.db")
    while True:
        price = bi_tra.get_current_price(client,bot.bot_info.symbol)
        print(price)
        bot.new_transaction(price)
        sinc.sinc_db_binance()
        time.sleep(10)


if __name__ == "__main__":
    # test_create_new_bot()
    
    # test_create_new_bot_buy_sell()
    # A skelleton dresed as king siting in a trone, with his hand holdin his head, in a foggy dungeon, his his green tunic.
    # test_kepp_alive_buy_sell()
    # test_get_all()
    while True:
        test_get_all()
        time.sleep(10)
    
    
    # test_create_new_bot()
    # keep_live()
    # price = bi_tra.get_current_price()
    # test_update()
    # 

    # bot = BotGridDolar(1)
    # bot.new_transaction(1.11)