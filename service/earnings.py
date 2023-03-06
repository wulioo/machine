import os
import pickle
import uuid

import pandas as pd
import datetime
import time

from django.core.cache import cache
from django.db.models import Q
from redis.exceptions import InvalidResponse

# celery_sharpe_earnings
from Machine.settings import PROCESS_NUM, BASE_DIR
from extra.db.models_tqmain import FutureDaily, EquityDaily
from utils.common import TimeContext, Common, func_time
from apps.future.tasks import celery_earnings
from celery.result import AsyncResult
from Machine.celery import app
from abc import ABCMeta, abstractmethod

from utils.exception import CommonException


class CalEarnings(metaclass=ABCMeta):
    sharpe: bool = False  # 是否计算 N日收益率/波动率

    @abstractmethod
    def cal_ear_by_price(self, wc_df, wc_list, label_ods):
        pass

    @abstractmethod
    def cal_ear_sharpe(self, wc_df, wc_list, label_ods):
        pass

    def _cal_label(self, val, od):
        try:
            data = 0 if val[f'sharpe_{od}'] == 0 else val[f'sharpe_{od}'] / val[f'pro_sharpe_std_{od}']

        except ZeroDivisionError as e:
            data = 0
        return data


class CloseEarnings(CalEarnings):
    price: str = 'close_price'

    # @func_time
    def cal_ear_by_price(self, wc_df, wc_list, label_ods):
        result = []
        label_cols = [f'label_{i}' for i in label_ods]
        for wc in wc_list:
            wc_df_sign = wc_df[wc_df['wind_code'] == wc]
            # 2.计算每一个wind_code收益率
            for od in label_ods:
                wc_df_sign[f'pro_{od}_close'] = wc_df_sign[self.price].shift(-od)
                wc_df_sign[f'label_{od}'] = (wc_df_sign[f'pro_{od}_close'] / wc_df_sign[self.price] - 1)
            result.append(wc_df_sign[['trading_date', 'wind_code'] + label_cols])
        return result

    def cal_ear_sharpe(self, wc_df, wc_list, label_ods):
        result = []
        label_cols = [f'label_{i}' for i in label_ods]
        for wc in wc_list:
            wc_df_sign = wc_df[wc_df['wind_code'] == wc]
            # 2.计算每一个wind_code收益率
            wc_df_sign['pre_close'] = wc_df_sign[self.price].shift(1)
            wc_df_sign['label'] = wc_df_sign[self.price] / wc_df_sign['pre_close'] - 1
            for od in label_ods:
                # 如果收益周期小于3 则跳过
                if od < 3:
                    wc_df_sign[f'label_{od}'] = 0
                    continue
                # 收益率（其实就是第一种标签）
                wc_df_sign[f'pro_{od}_close'] = wc_df_sign[self.price].shift(-od)
                wc_df_sign[f'sharpe_{od}'] = wc_df_sign[f'pro_{od}_close'] / wc_df_sign[self.price] - 1
                # 波动率
                wc_df_sign[f'sharpe_std_{od}'] = wc_df_sign['label'].rolling(od).std(ddof=0)
                wc_df_sign[f'pro_sharpe_std_{od}'] = wc_df_sign[f'sharpe_std_{od}'].shift(-od)
                # 收益率除以波动率得到第二种标签
                wc_df_sign[f'label_{od}'] = wc_df_sign.apply(lambda x: self._cal_label(x, od), axis=1)
            result.append(wc_df_sign[['trading_date', 'wind_code'] + label_cols])
        return result


class OpenEarnings(CalEarnings):
    price: str = 'open_price'

    def cal_ear_by_price(self, wc_df, wc_list, label_ods):
        result = []
        label_cols = [f'label_{i}' for i in label_ods]
        for wc in wc_list:
            wc_df_sign = wc_df[wc_df['wind_code'] == wc]
            # 2.计算每一个wind_code收益率
            # 1.使用下一交易日的开盘价
            wc_df_sign[self.price] = wc_df_sign[self.price].shift(-1)
            for od in label_ods:
                wc_df_sign[f'pro_{od}_open'] = wc_df_sign[self.price].shift(-od)
                wc_df_sign[f'label_{od}'] = wc_df_sign[f'pro_{od}_open'] / wc_df_sign[self.price] - 1
            result.append(wc_df_sign[['trading_date', 'wind_code'] + label_cols])
        return result

    def cal_ear_sharpe(self, wc_df, wc_list, label_ods):
        result = []
        label_cols = [f'label_{i}' for i in label_ods]
        for wc in wc_list:
            wc_df_sign = wc_df[wc_df['wind_code'] == wc]
            # 2.计算每一个wind_code收益率
            # 1.使用下一交易日的开盘价
            wc_df_sign[self.price] = wc_df_sign[self.price].shift(-1)
            # 计算 1 日收益率（用于计算收益率的波动率）
            wc_df_sign['pre_open'] = wc_df_sign[self.price].shift(1)
            wc_df_sign['label'] = wc_df_sign[self.price] / wc_df_sign['pre_open'] - 1
            for od in label_ods:
                # 如果收益周期小于3 则跳过
                if od < 3:
                    wc_df_sign[f'label_{od}'] = 0
                    continue
                wc_df_sign[f'pro_{od}_open'] = wc_df_sign[self.price].shift(-od)
                wc_df_sign[f'sharpe_{od}'] = wc_df_sign[f'pro_{od}_open'] / wc_df_sign[self.price] - 1
                wc_df_sign[f'sharpe_std_{od}'] = wc_df_sign['label'].rolling(od).std(ddof=0)
                wc_df_sign[f'pro_sharpe_std_{od}'] = wc_df_sign[f'sharpe_std_{od}'].shift(-od)
                wc_df_sign[f'label_{od}'] = wc_df_sign.apply(lambda x: self._cal_label(x, od), axis=1)
            result.append(wc_df_sign[['trading_date', 'wind_code'] + label_cols])
        return result


class FileEarnings(CalEarnings):
    price: str
    type_name: str

    def cal_ear_by_price(self, type_df, type_list, label_ods):
        result = []

        label_cols = [f'label_{i}' for i in label_ods]
        for tp in type_list:
            tp_df_sign = type_df[type_df[self.type_name] == tp]
            # 2.计算每一个wind_code收益率
            for od in label_ods:
                tp_df_sign[f'pro_{od}_file'] = tp_df_sign[self.price].shift(-od)
                tp_df_sign[f'label_{od}'] = (tp_df_sign[f'pro_{od}_file'] / tp_df_sign[self.price] - 1)
            result.append(tp_df_sign[['trading_date', self.type_name] + label_cols])
        return result

    def cal_ear_sharpe(self, wc_df, wc_list, label_ods):
        pass


class Earnings(metaclass=ABCMeta):

    def __init__(self, stime, etime, cal_ear: CalEarnings):
        self._stime = stime
        self._etime = etime
        self._cal_ear = cal_ear

    @property
    def cal_ear(self):
        return self._cal_ear

    @abstractmethod
    def _get_price(self, w_code, label_ods):
        pass

    def cal_earnings(self, f_df: pd.DataFrame, label_ods: list):
        """
        1.计算收益率
        2.celery版本
        :param df:
        :param label_ods:
        :param sharpe: 是否计算 N日收益率/波动率
        :return:
        """
        w_code = f_df['wind_code'].unique().tolist()
        wc_df = self._get_price(w_code, label_ods)
        result = self.__celery_earnings(w_code, wc_df, label_ods)
        pr_df = pd.concat(result, ignore_index=True)
        f_df["trading_date"] = pd.to_datetime(f_df["trading_date"], format="%Y-%m-%d")
        pr_df["trading_date"] = pd.to_datetime(pr_df["trading_date"], format="%Y-%m-%d")
        try:
            dfs = f_df.merge(pr_df, how='left', on=['trading_date', pr_df.columns[1]])
        except KeyError as e:
            raise CommonException(400, '标签因子合并失败!检查列名是否相同')
        return dfs

    def cal_file_earnings(self, file_one_df, file_two_df, label_ods: list):
        """
        1.计算上传文件的收益率
        2.celery版本
        :param file_one_df:
        :param file_two_df:
        :param label_ods:
        :return:
        """
        try:
            type_name_ab = file_two_df['type_name_ab'].unique().tolist()
        except KeyError as e:
            type_name_ab = file_two_df.iloc[:, 1].unique().tolist()
        self._cal_ear.price = file_two_df.columns.tolist()[2]
        self._cal_ear.type_name = file_two_df.columns.tolist()[1]
        result = self.__celery_earnings(type_name_ab, file_two_df, label_ods)
        # result = self.single_earnings(type_name_ab, file_two_df, label_ods)
        pr_df = pd.concat(result, ignore_index=True)
        file_one_df["trading_date"] = pd.to_datetime(file_one_df["trading_date"], format="%Y-%m-%d")
        pr_df["trading_date"] = pd.to_datetime(pr_df["trading_date"], format="%Y-%m-%d")
        try:
            dfs = file_one_df.merge(pr_df, how='left', on=['trading_date', pr_df.columns[1]])
        except KeyError as e:
            raise CommonException(400, '标签因子合并失败!检查列名是否相同')
        return dfs

    def __celery_earnings(self, w_or_t_list, price_df, label_ods):
        with TimeContext('收益率计算 cpu'):
            w_or_t_list = Common.list_slice_by_core(w_or_t_list)
            # d = self.single_earnings(w_or_t_list, price_df, label_ods)
            parma_id = f"cal_ear_{uuid.uuid1()}"
            cache.set(parma_id, {
                'ear': self,
                'price_df': price_df,
            })
            wc_dfs = [celery_earnings.delay(w_t_list, label_ods, parma_id) for w_t_list in w_or_t_list]
            result = []
            for res in wc_dfs:
                async_result = AsyncResult(id=str(res), app=app)
                async_result.wait()
                val = pd.read_json(async_result.get())
                val['trading_date'] = pd.to_datetime(val['trading_date'], unit='ms')
                result.append(val)
                async_result.forget()  # 将结果删除,执行完成，结果不会自动删除

            cache.delete(parma_id)

        return result

    def single_earnings(self, wc_list, price_df, label_ods):
        """
        单进程 DEBUG 调试版本
        :param wc_list:
        :param factor_df:
        :param price_df:
        :param label_ods:
        :return:
        """
        if self._cal_ear.sharpe:
            result = self._cal_ear.cal_ear_sharpe(price_df, wc_list, label_ods)
        else:
            result = self._cal_ear.cal_ear_by_price(price_df, wc_list, label_ods)

        return result

    def _get_future_time(self, label_ods):
        """
        多获取未来10天价格的time
        :return:
        """
        etime = datetime.datetime.strptime(self._etime, '%Y-%m-%d')
        # 2022-10-10 zdh 修改 10自然日修改成 25个自然日
        return etime + datetime.timedelta(days=max(label_ods) + 25)


class FutureEarnings(Earnings):

    def _get_price(self, w_code, label_ods):
        """
        1.从 future_daily 获取日期合约的收盘价close_price
        :return:
        """
        etime = self._get_future_time(label_ods)
        wc_df = FutureDaily.objects.using('tqmain') \
            .filter(Q(wind_code__in=w_code) & Q(trading_date__range=[self._stime, etime])) \
            .values('trading_date', 'wind_code', self._cal_ear.price).order_by('trading_date')
        return pd.DataFrame(wc_df)  # .to_json(orient='records', date_unit="s")


class EquityEarnings(Earnings):
    def _get_price(self, w_code, label_ods):
        """
       1.从 equity_daily 获取日期合约的收盘价close_price
       :return:
       """
        etime = self._get_future_time(label_ods)

        wc_df = EquityDaily.objects.using('tqmain') \
            .filter(Q(wind_code__in=w_code) & Q(trading_date__range=[self._stime, etime])) \
            .values('trading_date', 'wind_code', 'adj_factor', self._cal_ear.price).order_by('trading_date')
        df = pd.DataFrame(wc_df)
        # authority_price 复权价格
        df[self._cal_ear.price] = df[self._cal_ear.price] * df['adj_factor']
        return df
