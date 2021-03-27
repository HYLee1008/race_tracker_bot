import logging
import datetime

from src import official_api as ub
from src.unofficial_api import get_ohlcv


def operation_helper(data, target, operation):
    if operation == 'mean':
        output = [x[target] for x in data]
        output = sum(output) / len(output)

    elif operation == 'max':
        output = [x[target] for x in data]
        output = max(output)

    else:
        raise ValueError
    return output


def main():
    # How long?
    kernel_size = 10

    # For logging file
    log_file_name = "logbook.log"
    logger = logging.getLogger("main")
    logging.basicConfig(level=logging.INFO)

    stream_hander = logging.FileHandler(log_file_name, mode='a', encoding='utf8')
    logger.addHandler(stream_hander)

    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' : start racetracker')

    coins_list = ub.get_krw_tickers()

    # Current wallet state, store buy price
    activated_coin = {}

    while True:
        for coin in coins_list:
            data = get_ohlcv(coin, kernel_size + 1)

            if data is None:
                logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' : [Network Error] upbit network error')
                continue

            past_data = data[1:]
            current_data = data[0]

            current_price = current_data['tradePrice']
            
            if coin in activated_coin.keys():
                # sonjeol
                if current_price < activated_coin[coin] * 0.95:
                    order = ub.sell_coin(coin)
                    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' [SELL] coin : {coin}, upbit : {current_price}, order : {order}')
                    activated_coin.pop(coin, None)

                # sell coin when price is lower than MA10 
                elif current_price < operation_helper(past_data, 'tradePrice', 'mean'):
                    order = ub.sell_coin(coin)
                    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' [SELL] coin : {coin}, upbit : {current_price}, order : {order}')
                    activated_coin.pop(coin, None)

            else:
                if operation_helper(past_data, 'candleAccTradeVolume', 'max') * 3 < current_data['candleAccTradeVolume'] and operation_helper(past_data, 'tradePrice', 'max') < current_price:
                    # buy coin from upbit
                    order = ub.buy_coin(coin)
                    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' [BUY] coin : {coin}, upbit : {current_price}, order : {order}')
                    activated_coin[coin] = current_price




if __name__ == '__main__':
    main()