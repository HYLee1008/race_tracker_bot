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
def buy_coin(coin, price):
    wallet = pyupbit.Upbit(access_key, secret_key)

    krw = wallet.get_balance('KRW')
    orderbook = pyupbit.get_orderbook(coin)


    sell_price = orderbook[0]['orderbook_units'][0]['ask_price']
    sell_quantity = orderbook[0]['orderbook_units'][0]['bid_size']

    # difference = 100 * abs(sell_price - price) / min(sell_price, price)
    # if difference > 0.5:
    #     print(f"{coin} Too high difference : {price} / {sell_price}")
    #     return False

    # if krw > sell_price * sell_quantity:
    #     print(f"{coin} Not enough coin : {krw} {sell_price} {sell_price * sell_quantity}")
    #     return False

    unit = (krw / float(sell_price)) * 0.5

    order = wallet.buy_market_order(coin, unit)

    return order


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

    krw = wallet.get_balance('KRW')
    print(krw)
    print('good')
