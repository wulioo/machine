import json
import re
import uuid
import datetime
from typing import List
import itertools


import pandas as pd

from django.db import connections
from django.db.models import Q, Count, Sum
import django
import numpy as np

from extra.db.models_tqdailydrv import DwsTradingTimeFutureDaily
from logs import logger
from Machine.settings import PROCESS_NUM
from service.corr import CorrFactory
from service.earnings import Earnings
from service.layered import LayeredPosition, Layered, LayeredTest, LayeredBackTestIng
from service.night import NightTrading
from service.periods import PositioningPeriods
from service.varieties import Varieties

from utils.common import TimeContext, Common
from apps.future.tasks import celery_factor_diff, celery_factor_eq_diff, celery_ic
from utils.exception import CommonException
from abc import ABCMeta, abstractmethod

django.setup()
from extra.db.models_tqmain import FutureDominantDaily, FutureHeader, FutureDaily


class Factor(metaclass=ABCMeta):
    model = None
    column = None
    stime: str
    etime: str




class EquityFactor(Factor):
    index_code = None

    def get_eq_factor(self):
        if self.index_code == 'all':

            with TimeContext('queryset IO耗时：'):
                factor_arr = self.model.objects.using('tq_factor') \
                    .filter(trading_date__range=[self.stime, self.etime]) \
                    .values(*self.column, 'trading_date', 'wind_code') \
                    .order_by('wind_code', 'trading_date')
                df = pd.DataFrame(factor_arr)

        else:
            """使用原生sql"""
            from django.utils.connection import ConnectionProxy
            connection = ConnectionProxy(connections, 'tqmain')
            table = self.model._meta.db_table
            with connection.cursor() as cur:
                query_sql = f"""SELECT trading_date,wind_code,{','.join(self.column)} FROM `tq_factor`.`{table}`
                                    WHERE (`tq_factor`.`{table}`.wind_code,`tq_factor`.`{table}`.trading_date) in (
                                    SELECT
                                        `index_component`.`wind_code`
                                         ,`index_component`.`trading_date`
                                    FROM
                                        `tqmain`.`index_component`
                                    WHERE
                                        (
                                            `index_component`.`trading_date` BETWEEN '{self.stime}'
                                        AND '{self.etime}'
                                        AND `index_component`.`index_code` = '{self.index_code}')
                                    ) """
                cur.execute(query_sql)
                data = cur.fetchall()
                df = pd.DataFrame(data)
                if not df.empty:
                    df.columns = [i[0] for i in cur.description]
        return df


class FutureFactor(Factor):
    exchange = None

    def get_fv_factor(self, type_name_ab: list):
        """
       获取因子字段
       :param type_name_ab:
       :return:
       """
        factor_arr = self.get_factor_by_type(type_name_ab)
        # 4.从 future_dominant_daily 获取日期品种的主力合约
        join_method = 'right' if self.vari.vits != "all" else 'left'
        factor_arr = self.get_wd_by_type(factor_arr, type_name_ab, join_method)

        factor_arr.dropna(subset=['wind_code'], inplace=True)
        return factor_arr

    def get_factor_by_type(self, type_name_ab: list):
        return self.model.get_orderby_info_all(
            Q(trading_date__range=[self.stime, self.etime]) & Q(type_name_ab__in=type_name_ab),
            self.column + ['trading_date', 'type_name_ab'],
            ['type_name_ab', 'trading_date'], 'tq_factor')

    def get_typename_by_exchange(self):
        """
         根据 交易所 表来获取type_name_ab
         :return:
         """
        df = self.model.get_duplication_field('type_name_ab', 'tq_factor')
        df['exchange'] = df['type_name_ab'].str[-3:]
        type_name_ab = df[df['exchange'].isin(self.exchange)]['type_name_ab'].tolist()

        return type_name_ab

    def get_wd_by_type(self, factor_arr, type_name_ab, join_method='left'):
        """
        从 future_dominant_daily 获取日期品种的主力合约
        :param factor_arr:
        :param type_name_ab:
        :param join_method: 默认左连接
        :return:
        """

        fv_daily = FutureDominantDaily.get_orderby_info_all(
            Q(type_name_ab__in=type_name_ab) & Q(trading_date__range=[self.stime, self.etime]),
            ['trading_date', 'wind_code', 'type_name_ab'],
            ['type_name_ab', 'trading_date'], 'tqmain')
        # .将主力合约 trading_date type_name_ab,wind_code 和 因子表合并 f1 f2 f3
        factor_arr = factor_arr.merge(fv_daily, how=join_method, on=['trading_date', 'type_name_ab'])
        return factor_arr
