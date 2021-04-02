import logging
import datetime
import asyncio
import time
import functools

from src import official_api as ub
from src.unofficial_api import get_ohlcv

async def async_func(coin, logger, kernel_size, loop):
    is_buy = False

    while True:
        # if coin == 'KRW-BTC':
        #     start = time.time()

        data = await loop.run_in_executor(None, functools.partial(get_ohlcv, coin, kernel_size))

        if data is None:
            continue

        past_data = data[1:]
        current_data = data[0]

        current_price = current_data['tradePrice']

        if is_buy:
            # sonjeol
            if current_price < is_buy * 0.99:
                order = ub.sell_coin(coin)
                logger.info(datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S') + f' [SELL] coin : {coin}, upbit : {current_price}, order : {order}')
                is_buy = False

            # sell coin when price is lower than MA10
            elif current_price < operation_helper(past_data[:10], 'tradePrice', 'mean'):
                order = ub.sell_coin(coin)
                logger.info(datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S') + f' [SELL] coin : {coin}, upbit : {current_price}, order : {order}')
                is_buy = False

        else:
            if operation_helper(past_data, 'candleAccTradeVolume', 'max') * 3 < current_data[
                'candleAccTradeVolume'] and operation_helper(past_data, 'tradePrice', 'max') < current_price:
                # buy coin from upbit
                order = ub.buy_coin(coin)
                logger.info(datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S') + f' [BUY] coin : {coin}, upbit : {current_price}, order : {order}')
                is_buy = current_price
        # if coin == 'KRW-BTC':
        #     print(f'{coin} time : {time.time() - start}')



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


async def main(loop):
    kernel_size = 200

    # For logging file
    log_file_name = "logbook.log"
    logger = logging.getLogger("main")
    logging.basicConfig(level=logging.INFO)

    stream_hander = logging.FileHandler(log_file_name, mode='a', encoding='utf8')
    logger.addHandler(stream_hander)

    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' : start racetracker')

    coins_list = ub.get_krw_tickers()

    # Current wallet state, store buy price
    global activated_coin
    activated_coin = {}

    fts = [asyncio.ensure_future(async_func(coin, logger, kernel_size, loop)) for coin in coins_list]
    r = await asyncio.gather(*fts)
    global results
    results = r


if __name__ == '__main__':
    loop = asyncio.get_event_loop()  # 이벤트 루프를 얻음
    loop.run_until_complete(main(loop))  # main이 끝날 때까지 기다림
    loop.close()