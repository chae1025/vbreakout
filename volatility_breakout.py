import pyupbit
import datetime
import time


def cal_target(ticker):
    df = pyupbit.get_ohlcv(ticker, "day")
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    yesterday_range = yesterday['high']-yesterday['low']
    target = today['open'] + yesterday_range * 0.75
    return(target)
# can change "ticker" for any coin pairing with KRW

# 업비트 API
access = '123'
secret = '123'
upbit = pyupbit.Upbit(access, secret)

target = cal_target("KRW-BTC")
op_mode = False
hold = False

while True:
    now = datetime.datetime.now()

    # 매도
    if now.hour == 8 and now.minute == 59 and 00 <= now.second <= 10:
        if op_mode is True and hold is True:
            BTC_balance = upbit.get_balance("KRW-BTC")
            upbit.sell_market_order("KRW-BTC", BTC_balance)
            hold = False
        op_mode = False
        time.sleep(10)

    # 오후 9:00:20~30 목표가 갱신
    if now.hour == 9 and now.minute == 0 and 20 <= now.second <= 30:
        target = cal_target("KRW-BTC")
        op_mode = True

    price = pyupbit.get_current_price("KRW-BTC")

    # 매초마다 조건확인후 매수시도
    if op_mode is True and price is not None and price >= target and hold is False:
        krw_balance = upbit.get_balance("KRW")
        # 매수
        upbit.buy_market_order("KRW-BTC", krw_balance)
        hold = True

    # print (f"현재시간: {now} 목표가: {target} 현재가: {price} 보유상태: {hold} 동작상태: {op_mode}")

    time.sleep(1)
