import itertools
import json
import time
import uuid

import pandas as pd
from celery import shared_task
from django.core.cache import cache
from logs import logger
from service.corr import CorrFactory


@shared_task  # name表示设置任务的名称，如果不填写，则默认使用函数名做为任务名
def sequential_ic(uuid_df, tps):
    receive = cache.get(uuid_df)
    df = receive['df']
    factor = receive['factor']
    result = factor.single_seq_ic(df, tps)
    return result

