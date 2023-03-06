import json
import warnings

import requests as requests
from loguru import logger

warnings.filterwarnings('ignore')


class Api:
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
    }
    http: str = "https://192.168.1.166:8001"  # 测试环境请求地址
    # http: str = "http://127.0.0.1:8000"  # 本地环境请求地址
    @classmethod
    def post(cls, url: str, data):
        """
        :param url:  接口地址
        :param data: 接口参数
        :return:
        """
        resp = requests.post(f'{cls.http}/{url}', headers=cls.headers, data=json.dumps(data), verify=False)
        if resp.status_code != 201:
            logger.error(f"接口请求失败:{resp.json()['msg']}")
        return resp.json()

    @classmethod
    def get(cls, url, data):
        resp = requests.get(f'{cls.http}/{url}', headers=cls.headers, params=data, verify=False)
        if resp.status_code != 201:
            logger.error(f"接口请求失败:{resp.json()['msg']}")
        return resp.json()
