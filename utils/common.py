import time
from functools import wraps

import pandas as pd
from django.db.models import Q

from line_profiler import LineProfiler, line_profiler

from Machine.settings import PROCESS_NUM
from extra.db.models_tqfactor import FvFactorInfo
from extra.db.models_tqmain import TradingDateInfo
from extra.db.models_tqsignal import FvSignalInfo
from logs import logger
from utils.exception import ModelEmpty


class Common:
    @staticmethod
    def get_models(label, table):
        """
        反射获取模型
        :param label: 子模块
        :param table: 表名
        :return:
        """
        # 获取所有表名
        from django.apps import apps
        app = None
        m_obj = None
        # 获取类<FactorConfig: factor>
        for ap in apps.get_app_configs():
            if ap.label == label:
                app = ap
                break
        models = app.get_models(include_auto_created=True)

        for model in models:
            if table == model._meta.db_table:
                m_obj = model
                break
        if m_obj is None:
            logger.exception(f'{table}:不存在')
            raise ModelEmpty()
        return m_obj

    @classmethod
    def get_table(cls, factor_list, _db='tq_factor'):
        # 将重名的因子过滤
        repeat_factor = {}
        for factor in factor_list[:]:
            if '.' in factor:
                table_factor = factor.split('.')
                if repeat_factor.get(table_factor[0]):
                    repeat_factor[table_factor[0]].append(table_factor[1])
                else:
                    repeat_factor[table_factor[0]] = []
                    repeat_factor[table_factor[0]].append(table_factor[1])
                factor_list.remove(factor)
        if _db == "tq_factor":
            data = FvFactorInfo.get_info_all(Q(factor_name__in=factor_list), ['table_name', 'factor_name'], _db)
        else:
            data = FvSignalInfo.get_info_all(Q(factor_name__in=factor_list), ['table_name', 'factor_name'], _db)
        res = {}
        for key, val in data.iterrows():
            if res.get(val['table_name']):
                res[val['table_name']].append(val['factor_name'])
            else:
                res[val['table_name']] = []
                res[val['table_name']].append(val['factor_name'])
        for key, val in repeat_factor.items():
            if res.get(key):
                res[key] += val
            else:
                res[key] = val

        return res

    @staticmethod
    def list_slice_by_core(data):
        temp_list = []
        core = PROCESS_NUM
        temp_num = len(data) // core
        temp_yu = len(data) % core
        index_start = 0
        for i in range(core):
            if i < temp_yu:
                index_end = index_start + temp_num + 1
            else:
                index_end = index_start + temp_num
            if len(data[index_start:index_end]) > 0:
                temp_list.append(data[index_start:index_end])
            index_start = index_end
        return temp_list

    @staticmethod
    def get_previous_trading_time(td):
        """获取上一个交易日"""
        df = TradingDateInfo.get_dup_field_by_condition(Q(is_trading_date=1) & Q(nature_date__lt=td), 'nature_date', 'tqmain')
        df.sort_values(by='nature_date', inplace=True, ascending=False)
        td = df.iloc[0, 0]
        return td

    @staticmethod
    def get_next_trading_time(td):
        """获取下一个交易日"""
        df = TradingDateInfo.get_dup_field_by_condition(Q(is_trading_date=1) & Q(nature_date__gt=td), 'nature_date', 'tqmain')
        df.sort_values(by='nature_date', inplace=True, ascending=True)
        td = df.iloc[0, 0]
        return td

    @staticmethod
    def get_previous_interval_trading_time(td, interval):
        """获取上一个指定间隔交易日"""
        df = TradingDateInfo.get_dup_field_by_condition(Q(is_trading_date=1) & Q(nature_date__lte=td), 'nature_date', 'tqmain')
        df.sort_values(by='nature_date', inplace=True, ascending=False)
        td = df.iloc[interval, 0]
        return td


class TimeContext():
    """
    上下文管理器查看时间
    """

    def __init__(self, msg=None):
        self.msg = msg

    def __enter__(self):
        self.time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        logger.info(f'{self.msg} 耗时：{time.time() - self.time}')


# 查询接口中每行代码执行的时间
def func_time(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        profile = line_profiler.LineProfiler(f)  # 把函数传递到性能分析器
        profile.enable()  # 开始分析
        func_return = f(*args, **kwargs)
        profile.disable()  # 停止分析
        profile.print_stats()  # 打印出性能分析结果

        return func_return

    return decorator
