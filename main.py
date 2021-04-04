import asyncio
import aiohttp
import time
import datetime
import logging
from src import official_api as ub


def get_url_ohlcv(coin, count):
    return f'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.{coin}&count={count}'


async def get_ohlcv(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            return await res.json()

async def async_func(coin, count, logger):
    is_buy = False
    while True:
        if coin == 'KRW-BTC':
            start = time.time()

        data = await get_ohlcv(get_url_ohlcv(coin, count))

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
        if coin == 'KRW-BTC':
            print(f'{coin} time : {time.time() - start}')


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


async def main(coins_list, count, logger):
    await asyncio.gather(*[async_func(coin, count, logger) for coin in coins_list])


if __name__ == "__main__":
    kernel_size = 200

    # For logging file
    log_file_name = "logbook.log"
    logger = logging.getLogger("main")
    logging.basicConfig(level=logging.INFO)

    stream_hander = logging.FileHandler(log_file_name, mode='a', encoding='utf8')
    logger.addHandler(stream_hander)

    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' : start racetracker')

    coins_list = ub.get_krw_tickers()

    loop = asyncio.get_event_loop()          # 이벤트 루프를 얻음
    loop.run_until_complete(main(coins_list, kernel_size, logger))          # main이 끝날 때까지 기다림
