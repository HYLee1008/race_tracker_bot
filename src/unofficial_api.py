import datetime
import pandas as pd
import re

import requests
import socket

from requests.packages.urllib3.connection import HTTPConnection
from requests.adapters import HTTPAdapter
from requests.adapters import PoolManager
from urllib3.util.retry import Retry


class SockOpsAdapter(HTTPAdapter):
  def __init__(self, options, **kwargs):
    self.options = options
    super(SockOpsAdapter, self).__init__(**kwargs)

  def init_poolmanager(self, connections, maxsize, block=False):
    self.poolmanager = PoolManager(num_pools=connections,
                                   maxsize=maxsize,
                                   block=block,
                                   socket_options=self.options)


def _parse_remaining_req(remaining_req):
    """
    :param remaining_req:
    :return:
    """
    try:
        p = re.compile("group=([a-z]+); min=([0-9]+); sec=([0-9]+)")
        m = p.search(remaining_req)
        return m.group(1), int(m.group(2)), int(m.group(3))
    except:
        return None, None, None


def requests_retry_session(retries=5, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    """
    :param retries:
    :param backoff_factor:
    :param status_forcelist:
    :param session:
    :return:
    """
    options = HTTPConnection.default_socket_options + [
        (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
    ]

    s = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    # s.mount('http://', adapter)
    # s.mount('https://', adapter)
    s.mount('http://', SockOpsAdapter(options))
    s.mount('https://', SockOpsAdapter(options))
    return s


def _call_public_api(url, **kwargs):
    """
    :param url:
    :param kwargs:
    :return:
    """
    try:
        resp = requests_retry_session().get(url, params=kwargs)
        remaining_req_dict = {}
        remaining_req = resp.headers.get('Remaining-Req')
        if remaining_req is not None:
            group, min, sec = _parse_remaining_req(remaining_req)
            remaining_req_dict['group'] = group
            remaining_req_dict['min'] = min
            remaining_req_dict['sec'] = sec
        contents = resp.json()
        return contents, remaining_req_dict
    except Exception as x:
        print("It failed", x.__class__.__name__)
        return None



def get_url_ohlcv(coin, count):
    """
    candle에 대한 요청 주소를 얻는 함수
    :param interval: day(일봉), minute(분봉), week(주봉), 월봉(month)
    :return: candle 조회에 사용되는 url
    """

    url = f'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.{coin}&count={count}'

    return url


def get_ohlcv(coin, count):
    """
    캔들 조회
    :return:
    """
    try:
        url = get_url_ohlcv(coin, count)

        contents = _call_public_api(url)[0]

        return contents
    except Exception as x:
        print(x.__class__.__name__)
        return None

