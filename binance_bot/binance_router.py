from configparser import ConfigParser
from binance.spot import Spot
from datetime import datetime
import json
import pprint

# config_object = ConfigParser()
# config_object.read("config.ini")
# key_binance = config_object["keys"]

def get_info_about_pair(client:Spot, symbols:str):
    pair_info = client.exchange_info(symbol=symbols)
    return pair_info

def get_client_binance(api_key, api_secret ):
    client = Spot(api_key=api_key, api_secret=api_secret)
    return client

def get_transaction_satus(client:Spot, symbol = "EURBUSD", orderId="137633428"):
    # client = Spot(api_key=key_binance['api_key'], api_secret=key_binance['api_secret'])
    response = client.get_order(symbol,  orderId=orderId)
    return response

#BNBBRL
# THE BASE OF BNBBRL ARE THE BRL
# THE BASE OF EURBUSD are BUSD
def token_symbol_using_first(client:Spot, symbols, side, amount_token_base, price):
    def qnt_zeros(numero):
        # numero = numero
        contador = 0
        while numero < 1 :
            contador += 1
            numero = numero*10

        return contador

    ticker_info = client.ticker_price(symbols)
    if side == "BUY" and float(ticker_info["price"]) < price:
        print("buy more than the current price=", price)
        return False, None
    if side == "SELL" and float(ticker_info["price"]) > price:
        print("Sell less than the current price", price)
        return False, None

    pair_info = client.exchange_info(symbol=symbols)
    asset_precision = pair_info["symbols"][0]["baseAssetPrecision"]
    filter_s = list(filter(lambda x: x["filterType"] == "LOT_SIZE" , pair_info["symbols"][0]["filters"]))[0]
    filter_price_filter = list(filter(lambda x: x["filterType"] == "PRICE_FILTER" , pair_info["symbols"][0]["filters"]))[0]
    # step = qnt_zeros(float(filter_price_filter["tickSize"]))
    # here gets the quantity of the fraction
    step = qnt_zeros(float(filter_s['stepSize']))
    # step = filter_s['stepSize'].rfind("1")
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
        try:
            response = client.new_order(**params)
            return True, response
        except:
            return False, {}
    else: 
        return False, {}

def token_symbol_using_base(client:Spot, symbols, side, amount_token_base, price):
    ticker_info = client.ticker_price(symbols)
    if side == "BUY" and float(ticker_info["price"]) < price:
        print("buy more than the current price", price)
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
# 139541366
def get_current_price(client:Spot, symbol='EURBUSD'):
    # client = Spot(api_key=key_binance['api_key'], api_secret=key_binance['api_secret'])
    ticker_info = client.ticker_price(symbol)
    print(ticker_info)
    return round(float(ticker_info["price"]), 4)

#  response = client.get_order("BTCUSDT", orderId="")
def create_new_order(client, symbol='EURBUSD',type="SELL", qnt_base=11.9, price=1.06 ):
    # client = Spot(api_key=key_binance['api_key'], api_secret=key_binance['api_secret'])
    r_worked, response = token_symbol_using_first(client, symbol, type,  qnt_base, price )

    return r_worked, response

def get_user_asset_qnt(client:Spot, symbol:str, qnt_round=4):
    # client = Spot(api_key=key_binance['api_key'], api_secret=key_binance['api_secret'])
    # res = client.coin_info()
    # res = client.asset_detail()
    res = client.user_asset(asset=symbol)[0]

    res["total"] = float(res["free"]) + float(res["locked"]) + float(res["freeze"]) + float(res["withdrawing"]) + float(res["ipoable"])
    res["time_ms"] = int(datetime.now().timestamp()*1000)
    if(symbol == "BUSD"):
        res["PAIRBUSD"] = 1
    elif(symbol.upper() == "BRL"):
        res["PAIRBUSD"] = str(get_current_price(client,"BUSDBRL"))
    else:
        res["PAIRBUSD"] = str(get_current_price(client,symbol.upper()+"BUSD"))

    res["BUSDBRL"] = str(get_current_price(client, "BUSDBRL"))
    return res

def get_historical_k_line(pair="EURBUSD", time_step = "1h", datetime_str = '20/12/22'):
    def convert_to_kline(ls):
        di = {
            "pair": pair,
            "time_step": time_step,
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
    
    time_1 = datetime_str
    if type(datetime_str) == str:
        datetime_object = datetime.strptime(datetime_str, '%d/%m/%y')
        time_1 = int(datetime_object.timestamp()*1000)
    
    spot_client = Spot()
    k_lines = list(map(convert_to_kline, spot_client.klines(pair, time_step, limit=1000, startTime = time_1)))

    if type(datetime_str) == str:
        return k_lines, k_lines[0]["open_time_ms"], k_lines[-1]["open_time_ms"]
    else:
        return k_lines[1:], k_lines[1]["open_time_ms"], k_lines[-1]["open_time_ms"]

def test_1():

    client = Spot()
    client = Spot(api_key=key_binance['api_key'], api_secret=key_binance['api_secret'])
    # BUY EURO POR USD USANDO O FIRST USANDO EURO
    
    # VENDE EURO POR USD USANDO O FIRST USANDO EURO
    r_worked, response = token_symbol_using_first(client, 'EURBUSD', "SELL", 11.9, 1.0653 ) # vendendo 12 euro a 1.14

    # r_worked, response = token_symbol_using_first(client, 'EURBUSD', "BUY", 11.6, 1.065 ) # comprando 11.6 euro a 1.04
    # response = token_symbol_using_base(client, 'EURBUSD', "BUY", 12, 1.04 ) # comprando 12 euro a 1.04
    # response1 = token_symbol_using_base(client, 'EURBUSD', "BUY", 12, 1.06 )
    # response = buy_token_symbol_using_base(client, 'BNBBRL', "BUY", 11, 1600 )
    # print(response)
    # response = buy_token_symbol_using_base(client, 'BNBBRL', "SELL", 11, 1600 )
    with open(f"test_{response['status']}_sell_{response['orderId']}.json", "w") as file:
        file.write(json.dumps(response))

    # order_status = client.get_order("EURBUSD", orderId=response['orderId']) # STATUS NEW, CANCELED
    
    # print(response)
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

def test_4():
    k_lines, first_k_line, last_k_line = get_historical_k_line("EURBUSD", "5m", 1671794100000) # if put some timestamp get all less the passing.
    print(first_k_line, last_k_line )

def test_5():
    client = Spot(api_key=key_binance['api_key'], api_secret=key_binance['api_secret'])
    
    response = client.get_order("EURBUSD", orderId="137633428")
    with open(f"test_{response['status']}_{response['orderId']}.json", "w") as file:
        file.write(json.dumps(response))
    print(response)

def test_6():
    print(get_current_price())

def test_7():
    # client = Spot(api_key=key_binance['api_key'], api_secret=key_binance['api_secret'])
    # res = client.coin_info()
    # res = client.asset_detail()
    res = get_user_asset_qnt("EUR")
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(res)
    res = get_user_asset_qnt("BUSD")
    pp.pprint(res)
    # print(res)

def test_8():
    def qnt_zeros(numero):
        # numero = numero
        contador = 0
        while numero < 1 :
            contador += 1
            numero = numero*10

        return contador

    spot_client = Spot()
    symbols = "BTCBRL"
    info = get_info_about_pair(spot_client, symbols)
    pair_info = spot_client.exchange_info(symbol=symbols)
    # asset_precision = pair_info["symbols"][0]["baseAssetPrecision"]
    filter_s = list(filter(lambda x: x["filterType"] == "LOT_SIZE" , pair_info["symbols"][0]["filters"]))[0]
    price_precision = qnt_zeros(float(list(filter(lambda x: x["filterType"] == "PRICE_FILTER" , pair_info["symbols"][0]["filters"]))[0]["tickSize"]))
    print(f"o preco pode ter ate {price_precision} casas decimais")
    # precision da quantidade 
    qunt_moeda_precision = qnt_zeros(float(filter_s['stepSize']))
    print(f"a quantidade de moedas negociadsa pode ter até {qunt_moeda_precision} casas decimais")
    
    # step = filter_s['stepSize'].rfind("1")
    min_qnt = float(list(filter(lambda x: x["filterType"] == "LOT_SIZE" , pair_info["symbols"][0]["filters"]))[0]["minQty"])

    print(info)


if __name__ == "__main__":
    test_8()
    # test_6()
    # test_1()
    # test_5()
    # test_2()
    # test_3()
    # test_4()
    
    
    

    

    


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




