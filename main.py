import time
import logging
import datetime

import upbit as ub


def main():
    # For logging file
    log_file_name = "logbook.log"
    logger = logging.getLogger("main")
    logging.basicConfig(level=logging.INFO)

    stream_hander = logging.FileHandler("flow.log", mode='a', encoding='utf8')
    logger.addHandler(stream_hander)

    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' : start racetracker')

    coins_list = ub.get_krw_tickers()

    # Current wallet state, store buy price
    activated_coin = {}

    while True:
        for coin in coins_list:
            time.sleep(0.07)
            df = ub.get_ohlcv(coin)

            if df is None:
                logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' : [Network Error] upbit network error')
                continue

            past_data = df[:-1]
            current_data = df[-1:]

            current_price = current_data['close'].values[0]
            
            if coin in activated_coin.keys():
                # sonjeol
                if current_price < activated_coin[coin] * 0.95:
                    order = ub.sell_coin(coin)
                    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' [SELL] coin : {coin}, upbit : {current_price}, order : {order}')
                    activated_coin.pop(coin, None)

                # sell coin when price is lower than MA10 
                elif current_price < past_data['close'][-10:].mean():
                    order = ub.sell_coin(coin)
                    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' [SELL] coin : {coin}, upbit : {current_price}, order : {order}')
                    activated_coin.pop(coin, None)

            else:
                if past_data['volume'].max() * 3 < current_data['volume'].values[0] and past_data['high'].max() < current_price:
                    # buy coin from upbit
                    order = ub.buy_coin(coin)
                    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' [BUY] coin : {coin}, upbit : {current_price}, order : {order}')
                    activated_coin[coin] = current_price


if __name__ == '__main__':
    # main()
    df = ub.get_ohlcv("KRW-BTC")
    print(df['close'][-10:].mean())