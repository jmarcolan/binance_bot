from dataclasses import dataclass

@dataclass
class K_line:
    kline_id: int
    open_time_ms: int
    open_price: str
    high_prioce: str
    low_price: str
    close_price: str
    volume: str
    close_time_ms:int
    asset_volume: str
    number_trade: int
    taker_buy_base_vol: str
    takes_buy_queote_vol: str
    ignore: str