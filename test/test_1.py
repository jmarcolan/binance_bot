import time

import binance_bot.create_account as ca
import binance_bot.create_bot as cb

ca.test_1()
ca.test_2()
cb.test_create_new_bot()


while True:
    cb.test_get_all()
    time.sleep(10)
