from configparser import ConfigParser
from binance.spot import Spot
from datetime import datetime

config_object = ConfigParser()
config_object.read("config.ini")
key_binance = config_object["keys"]







#BNBBRL
# THE BASE OF BNBBRL ARE THE BRL
# THE BASE OF EURBUSD are BUSD
def token_symbol_using_first(client:Spot, symbols, side, amount_token_base, price):
    ticker_info = client.ticker_price(symbols)
    if side == "BUY" and float(ticker_info["price"]) < price:
        print("buy more than the current price")
        return False, None
    if side == "SELL" and float(ticker_info["price"]) > price:
        print("Sell less than the current price")
        return False, None

    pair_info = client.exchange_info(symbol=symbols)
    asset_precision = pair_info["symbols"][0]["baseAssetPrecision"]
    filter_s = list(filter(lambda x: x["filterType"] == "LOT_SIZE" , pair_info["symbols"][0]["filters"]))[0]
    step = filter_s['stepSize'].rfind("1") - 1
    min_qnt = float(list(filter(lambda x: x["filterType"] == "LOT_SIZE" , pair_info["symbols"][0]["filters"]))[0]["minQty"])

    # if side == "BUY":
    # qnt_ask = amount_token_base/price*1
    qnt_ask = amount_token_base
    r_more_than_need = qnt_ask > min_qnt

    if r_more_than_need:
        params = {
        'symbol': symbols,
        'side': side,
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': float('{:.{prec}f}'.format(qnt_ask, prec=step)),
        'price': price
        }
        response = client.new_order(**params)
        return True, response
    else: 
        return False, None

def token_symbol_using_base(client:Spot, symbols, side, amount_token_base, price):
    ticker_info = client.ticker_price(symbols)
    if side == "BUY" and float(ticker_info["price"]) < price:
        print("buy more than the current price")
        return False, None
    if side == "SELL" and float(ticker_info["price"]) > price:
        print("Sell less than the current price")
        return False, None

    pair_info = client.exchange_info(symbol=symbols)
    asset_precision = pair_info["symbols"][0]["baseAssetPrecision"]
    filter_s = list(filter(lambda x: x["filterType"] == "LOT_SIZE" , pair_info["symbols"][0]["filters"]))[0]
    step = filter_s['stepSize'].rfind("1") - 1
    min_qnt = float(list(filter(lambda x: x["filterType"] == "LOT_SIZE" , pair_info["symbols"][0]["filters"]))[0]["minQty"])

    # if side == "BUY":
    qnt_ask = amount_token_base/price*1
    # qnt_ask = amount_token_base
    r_more_than_need = qnt_ask > min_qnt

    if r_more_than_need:
        params = {
        'symbol': symbols,
        'side': side,
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': float('{:.{prec}f}'.format(qnt_ask, prec=step)),
        'price': price
        }
        response = client.new_order(**params)
        return True, response
    else: 
        return False, None



def get_historical_k_line(time_step = "1h", datetime_str = '20/12/22'):
    def convert_to_kline(ls):
        di = {
            "open_time_ms": ls[0],
            "open_price":  ls[1],
            "high_prioce": ls[2],
            "low_price":   ls[3],
            "close_price": ls[4],
            "volume":      ls[5],
            "close_time_ms": ls[6],
            "asset_volume": ls[7],
            "number_trade": ls[8],
            "taker_buy_base_vol": ls[9],
            "takes_buy_queote_vol": ls[10],
            "ignore": ls[11],
        }
        return di
    
    
    datetime_object = datetime.strptime(datetime_str, '%d/%m/%y')
    time_1 = int(datetime_object.timestamp()*1000)
    spot_client = Spot()
    k_lines = list(map(convert_to_kline, spot_client.klines("EURBUSD", time_step, limit=1000, startTime = time_1)))
    return k_lines, k_lines[0]["open_time_ms"], k_lines[-1]["open_time_ms"]

# {'symbol': 'EURBUSD', 'orderId': 134115308, 'orderListId': -1, 'clientOrderId': 'AUJeEtlqm64jDfkIP187nR', 'transactTime': 1674336191960, 'price': '1.07000000', 'origQty': '10.40000000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'BUY', 'workingTime': 1674336191960, 'fills': [], 'selfTradePreventionMode': 'NONE'}

# def token_symbol_using_base(client:Spot, symbols, side, amount_token_base):

#  response = client.get_order("BTCUSDT", orderId="")
def test_1():
    client = Spot()
    client = Spot(api_key=key_binance['api_key'], api_secret=key_binance['api_secret'])
    # BUY EURO POR USD USANDO O FIRST USANDO EURO
    
    # VENDE EURO POR USD USANDO O FIRST USANDO EURO
    response = token_symbol_using_first(client, 'EURBUSD', "SELL", 11.9, 1.14 ) # vendendo 12 euro a 1.14

    response = token_symbol_using_first(client, 'EURBUSD', "BUY", 11.9, 1.04 ) # comprando 12 euro a 1.04
    # response = token_symbol_using_base(client, 'EURBUSD', "BUY", 12, 1.04 ) # comprando 12 euro a 1.04
    # response1 = token_symbol_using_base(client, 'EURBUSD', "BUY", 12, 1.06 )
    # response = buy_token_symbol_using_base(client, 'BNBBRL', "BUY", 11, 1600 )
    # print(response)
    # response = buy_token_symbol_using_base(client, 'BNBBRL', "SELL", 11, 1600 )
    print(response)
    # print(response1)
    # https://github.com/binance/binance-connector-python


def test_2():
    spot_client = Spot()
    k_lines = spot_client.klines("EURBUSD", "1h", limit=1000)
    print(k_lines)
    print(len(k_lines))

def test_3():
    k_lines, first_k_line, last_k_line = get_historical_k_line("5m")
    print(first_k_line, last_k_line )
    
if __name__ == "__main__":
    # test_1()
    # test_2()
    test_3()
    
    

    

    


# # Get server timestamp
# print(client.time())
# # Get klines of BTCUSDT at 1m interval
# print(client.klines("BTCUSDT", "1m"))
# # Get last 10 klines of BNBUSDT at 1h interval
# print(client.klines("BNBUSDT", "1h", limit=10))

# API key/secret are required for user data endpoints


# Get account and balance information
# balances = client.account()
# ls_tokens = list(filter(lambda x: float(x["free"]) > 0, balances["balances"]))
# print(ls_tokens)

# # Post a new order
# ticker = client.book_ticker("BNBBRL")

# params = {
#     'symbol': 'BNBBRL',
#     'side': 'BUY',
#     'type': 'LIMIT',
#     'timeInForce': 'GTC',
#     'quantity': 11,
#     'price': 1700
# }
# response = client.new_order(**params)




