import pyupbit


access_key = 'XS5bMcecpljFvMJcQJxBkIK3a64Xw8VwQxcdrZWT'
secret_key = '5M6DE5VRKUzFM237jVDFZcAQdVsPaZxrSzNXURbL'


# get KRW tickers
def get_krw_tickers():
    tickers = pyupbit.get_tickers(fiat='KRW')
    return tickers

# get current price of the coins
def get_current_price(coins):
    return pyupbit.get_current_price(coins)

# get past data
def get_ohlcv(coin):
    return pyupbit.get_ohlcv(coin, interval='minute1')


# buy coin
def buy_coin(coin):
    try:
        wallet = pyupbit.Upbit(access_key, secret_key)

        krw = wallet.get_balance('KRW')

        order = wallet.buy_market_order(coin, krw * 0.5)

        return order
    except:
        return False

# sell coin
def sell_coin(coin):
    try:
        wallet = pyupbit.Upbit(access_key, secret_key)
        
        unit = wallet.get_balance(coin)

        order = wallet.sell_market_order(coin, unit)

        return order
    except:
        return False


if __name__ == '__main__':
    wallet = pyupbit.Upbit(access_key, secret_key)

    order = sell_coin("KRW-BTC")
    print(order)
