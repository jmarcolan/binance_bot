from dataclasses import dataclass
import sqlalchemy


from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from datetime import datetime

# @dataclass
# class K_line:
#     kline_id: int
#     open_time_ms: int
#     open_price: str
#     high_prioce: str
#     low_price: str
#     close_price: str
#     volume: str
#     close_time_ms:int
#     asset_volume: str
#     number_trade: int
#     taker_buy_base_vol: str
#     takes_buy_queote_vol: str
#     ignore: str


class Base(DeclarativeBase):
    pass

class K_line_h(Base):
    __tablename__ = 'K_line'

    # id = Column(Integer(), auto_increment=True, primary_key=True)
    # name = Column(String(50), nullable=False)
    # age = Column(Integer(), nullable=False)
    kline_id=  Column(Integer(), auto_increment=True, primary_key=True)
    pair = Column(String(100), nullable=False)
    time_step  = Column(String(100), nullable=False)
    # kline_id= Column(Integer(), nullable=False)
    open_time_ms= Column(Integer(), nullable=False)
    open_price = Column(String(100), nullable=False)
    high_prioce= Column(String(100), nullable=False)
    low_price= Column(String(100), nullable=False)
    close_price= Column(String(100), nullable=False)
    volume= Column(String(100), nullable=False)
    close_time_ms= Column(Integer(), nullable=False)
    asset_volume= Column(String(100), nullable=False)
    number_trade= Column(Integer(), nullable=False)
    taker_buy_base_vol= Column(String(100), nullable=False)
    takes_buy_queote_vol= Column(String(100), nullable=False)
    ignore= Column(String(100), nullable=False)

    def __repr__(self):
        return f'<Kline pair="{self.pair}" time= {self.open_time_ms} , {datetime.fromtimestamp(self.open_time_ms/1000)} time_step={self.time_step} close_p = "{self.close_price}"'



class B_transaction(Base):
    __tablename__ = 'B_transaction'
    symbol= Column(String(100))
    orderId=  Column(Integer(), primary_key=True)
    orderListId= Column(Integer())
    clientOrderId= Column(String(100))
    transactTime = Column(Integer())
    price= Column(String(100))
    origQty= Column(String(100))
    executedQty= Column(String(100))
    cummulativeQuoteQty= Column(String(100))
    status= Column(String(100))
    timeInForce= Column(String(100))
    type= Column(String(100))
    side= Column(String(100))
    stopPrice= Column(String(100))
    icebergQty= Column(String(100))
    time= Column(Integer())
    updateTime = Column(Integer())
    isWorking= Column(Boolean())
    workingTime= Column(Integer())
    origQuoteOrderQty= Column(String(100))
    selfTradePreventionMode= Column(String(100))

    def __repr__(self):
        return f"orderid = {self.orderId} ,symbol = {self.symbol}, "

class Bot_info(Base):
    __tablename__ = 'Bot_info'
    bot_id      =  Column(Integer(), auto_increment=True, primary_key=True)
    count_id   = Column(Integer())
    status = Column(String(100)) # ACTIVATED
    symbol      = Column(String(100))
    delta_price = Column(String(100))
    bot_price   = Column(String(100))
    top_price   = Column(String(100))
    quantity    = Column(String(100))
    type_bot    = Column(String(100))
    
    def __repr__(self):
        return f"orderid = {self.bot_id} ,symbol = {self.symbol}"

class Bot_tran(Base):
    __tablename__ = 'Bot_tran'
    ts_id =  Column(Integer(), auto_increment=True, primary_key=True)
    # count_id   = Column(Integer())
    bot_id = Column(Integer())
    symbol = Column(String(100)) 
    sell_id     = Column(Integer())
    sell_status = Column(String(100)) # [WAIT, WAIT_BUY, NEW, FILLED, CANCELED]
    sell_price  = Column(String(100))
    sell_qnt    = Column(String(100))

    buy_id    = Column(Integer())
    buy_satus = Column(String(100)) # [WAIT, WAIT_SELL, NEW, FILLED, CANCELED]
    buy_price  = Column(String(100))
    buy_qnt    = Column(String(100))
    
    def __repr__(self):
        return f"`{self.ts_id} / bot={self.bot_id}, s_id= {self.sell_id}"

class Account(Base):
    __tablename__ = 'Account'
    count_id   = Column(Integer(), auto_increment=True, primary_key=True)
    api_key    = Column(String(300))
    api_secret = Column(String(300))
    name       = Column(String(300))
    password   = Column(String(300))
    def __repr__(self):
        return f"{self.count_id} ,name={self.name}"

class Bot_account_coin_history(Base):
    __tablename__ = 'Bot_account_coin_history'
    hist_id =  Column(Integer(), auto_increment=True, primary_key=True)
    count_id = Column(Integer())
    BUSDBRL = Column(String(100))
    EURBUSD = Column(String(100))
    asset = Column(String(100))
    btcValuation =  Column(String(100))
    free = Column(String(100))
    freeze = Column(String(100))
    ipoable = Column(String(100))
    locked = Column(String(100))
    time_ms = Column(Integer())
    total = Column(String(100))
    withdrawing = Column(String(100))

    def __repr__(self):
        return f"`{self.count_id} / bot={self.hist_id},total={self.total}, time{self.time_ms}"
    # 
# {ts_id, bot_id, buy_id, buy_satus:[new, filled, cancel], buy_qnt, sell_qnt, 
# sell_id, sell_status:[new, filled, cancel], sell_qnt, sell_price}
# 
# {bot_id, delta_price[0.01], bot_price[ 0.8], top_price[1.2] pair [EURBUSD]0}
# Connect to database


# class Student(Base):
#     __tablename__ = 'students'

#     id = Column(Integer(), auto_increment=True, primary_key=True)
#     name = Column(String(50), nullable=False)
#     age = Column(Integer(), nullable=False)

#     def __repr__(self):
#         return f'<Student name="{self.name}" age={self.age}>'
    

# if __name__ == "__main__":
# # engine = sqlalchemy.create_engine("sqlite:///:memory:")
#     engine = sqlalchemy.create_engine("sqlite:////home/app/data/demo.db")

#     Base.metadata.create_all(engine)

#     with Session(engine) as session:
#         spongebob = Student(
#             name="spongebob",
#             age=20
#             #  addresses=[Address(email_address="spongebob@sqlalchemy.org")],
#         )
        
#         session.add_all([spongebob])
#         session.commit()



# session = Session(bind=engine)
