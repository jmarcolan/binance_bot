from configparser import ConfigParser
from binance.spot import Spot
config_object = ConfigParser()
config_object.read("config.ini")
key_binance = config_object["keys"]

#BNBBRL
# THE BASE OF BNBBRL ARE THE BRL
def buy_token_symbol_using_base(client:Spot, symbols, side, amount_token_base, price):
    ticker_info = client.ticker_price("BNBBRL")
    if side == "BUY" and float(ticker_info["price"]) < price:
        print("buy more than the current price")
        return False, None
    if side == "SELL" and float(ticker_info["price"]) > price:
        print("Sell less than the current price")
        return False, None

    pair_info = client.exchange_info(symbol="BNBBRL")
    asset_precision = pair_info["symbols"][0]["baseAssetPrecision"]
    filter_s = list(filter(lambda x: x["filterType"] == "LOT_SIZE" , pair_info["symbols"][0]["filters"]))[0]
    step = filter_s['stepSize'].rfind("1") - 1
    min_qnt = float(list(filter(lambda x: x["filterType"] == "LOT_SIZE" , pair_info["symbols"][0]["filters"]))[0]["minQty"])

    # if side == "BUY":
    qnt_ask = amount_token_base/price*1.01
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
    

def test_1():
    client = Spot()
    client = Spot(api_key=key_binance['api_key'], api_secret=key_binance['api_secret'])
    response = buy_token_symbol_using_base(client, 'BNBBRL', "BUY", 11, 1600 )
    print(response)
    response = buy_token_symbol_using_base(client, 'BNBBRL', "SELL", 11, 1600 )
    print(response)


    
if __name__ == "__main__":
    test_1()



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




