import pyupbit

# api 관련.
access_key = "AAPWbiqKibiFVREqoTfy0wj3WgTPVK4otjub7QLo"
secret_key = "oqXYFxvflQhoHThaeQNhuFSpegVxPjQxceh5Ep7r"
server_url = "https://api.upbit.com/v1/orders"
upbit = pyupbit.Upbit(access_key, secret_key)

# 0.0 ~ 1.0 사이의 result값에 따라 매수, 매도 결정.
def upbitSale1(result):
    price_crnt = pyupbit.get_current_price(["KRW-BTC"])     # 현재가.
    balance = upbit.get_balance(ticker="KRW-BTC")     # 보유 수량.
    if result[1] >= 0.9 and result[0] <= 0.25:
        print("매수 : ", upbit.buy_market_order("KRW-BTC", (price_crnt * balance) / 30))  # 해당 코인의 보유 가치의 3%만큼 매수.
    elif result[0] >= 0.8 and result[1] <= 0.25:
        print("매도 : ", upbit.sell_limit_order("KRW-BTC", price_crnt, balance / 30))  # 해당 보유 코인의 3% 갯수만큼 시장가에 매도.

def upbitSale2(result):
    price_crnt = pyupbit.get_current_price(["KRW-BTC"])     # 현재가.
    balance = upbit.get_balance(ticker="KRW-BTC")     # 보유 수량.
    if result[1] >= 0.8 and result[0] <= 0.3:
        print("매수 : ", upbit.buy_market_order("KRW-BTC", (price_crnt * balance) / 30))  # 해당 코인의 보유 가치의 3%만큼 매수.
    elif result[0] >= 0.7 and result[1] <= 0.3:
        print("매도 : ", upbit.sell_limit_order("KRW-BTC", price_crnt, balance / 30))  # 해당 보유 코인의 3% 갯수만큼 시장가에 매도.


# Softmax용.
def upbitSale3(result):
    price_crnt = pyupbit.get_current_price(["KRW-BTC"])     # 현재가.
    balance = upbit.get_balance(ticker="KRW-BTC")     # 보유 수량.
    if result >= 0.87:
        print("매수 : ", upbit.buy_market_order("KRW-BTC", (price_crnt * balance) / 30))  # 해당 코인의 보유 가치의 3%만큼 매수.
    elif result <= 0.15:
        print("매도 : ", upbit.sell_limit_order("KRW-BTC", price_crnt, balance / 30))  # 해당 보유 코인의 3% 갯수만큼 시장가에 매도.