from dataclasses import dataclass
import sqlalchemy


from sqlalchemy import Column, String, Integer
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
