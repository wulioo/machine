import itertools
import json
import uuid
from abc import ABCMeta, abstractmethod

import numpy
import pandas as pd
from django.core.cache import cache
from pandas import Series

from Machine.settings import PROCESS_NUM
from utils.common import TimeContext, Common
from utils.exception import CommonException
from apps.future.tasks import celery_layered, celery_backtesting
from celery.result import AsyncResult
from Machine.celery import app


class Layered(metaclass=ABCMeta):

    def __init__(self):
        self.num = None
        self._instr_per_group = None

    @property
    def instr_per_group(self):
        return self._instr_per_group


class LayeredTest(Layered):
    def celyer_group_cumsum(self, wc_and_erg, factor_list, periods_list):
        """多进程版本"""
        # 6.分层测试
        factor_group_label = list(itertools.product(factor_list, self.num, periods_list))
        fgl = Common.list_slice_by_core(factor_group_label)

        uuid_df = f"layere_df_{uuid.uuid1()}"
        cache.set(uuid_df, {
            'df': wc_and_erg,
            'factor': self
        })
        result = [celery_layered.delay(f,uuid_df) for f in fgl]
        temp_df = {}
        with TimeContext(f'分层总时长 cpu'):
            for res in result:
                async_result = AsyncResult(id=str(res), app=app)
                async_result.wait()
                asy_res = async_result.get()
                for key, val in asy_res.items():
                    if not temp_df.get(key):
                        temp_df[key] = val
                    else:
                        for group, data in val.items():
                            if not temp_df[key].get(group):
                                temp_df[key][group] = data
                            else:
                                temp_df[key][group].update(data)
                async_result.forget()
            cache.delete(uuid_df)
        return temp_df

    def single_group_cumsum(self, wc_and_erg, f):
        """单进程版本"""

        result = {}
        for factor, n_group, holding_od in f:
            label_col = f'label_{holding_od}'
            if not result.get(factor):
                result[factor] = {}
            if not result[factor].get(n_group):
                result[factor][n_group] = {}

            with TimeContext(f'计算单因子-{factor}-{n_group}-{holding_od} cpu'):
                wc_and_erg['trading_date'] = pd.to_datetime(wc_and_erg['trading_date'], unit='s')

                # 1.drop 掉收益率为空的行
                df_no_nan = wc_and_erg.dropna(subset=[label_col, factor])
                # 初始化以交易日为 index，各层为 columns 的 df
                tds = df_no_nan['trading_date'].astype(str).unique().tolist()
                tds = sorted(tds)
                group_return = pd.DataFrame(index=tds, columns=[f'group{i + 1}' for i in range(n_group)])
                group_return.index.rename('trading_date', inplace=True)

                for td in tds:
                    td_df = df_no_nan[df_no_nan['trading_date'] == td]
                    td_df.sort_values(by=[factor, td_df.columns[1]], ascending=[False, True], inplace=True, ignore_index=True)
                    avg_ret = td_df[label_col].mean()
                    instr_per_group = len(td_df) / n_group

                    for i in range(n_group):
                        group_avg_ret = td_df[label_col].iloc[
                                        round(i * instr_per_group):round((i + 1) * instr_per_group)].mean()
                        group_return.loc[td, f'group{i + 1}'] = group_avg_ret - avg_ret

                # 按持有天数间隔交易日
                tds = group_return.index.tolist()[::holding_od]
                group_return = group_return.loc[tds]

                # 各层超额收益率累加后 +1
                for i in range(n_group):
                    group_return[f'group{i + 1}'] = (group_return[f'group{i + 1}']).cumsum() + 1

                """
                数据格式转换返回前端
                :param data:
                :return:
                """

                temp_arr = []
                for group_k, group_v in group_return.items():
                    temp_dict = {
                        'name': group_k,
                        'type': 'line',
                        'data': list(group_v),
                        'showSymbol': False,
                    }
                    temp_arr.append(temp_dict)

                temp_arr.append(list(group_return.index))
                result[factor][n_group][label_col] = temp_arr
        return result


class LayeredPosition(Layered):
    money: float
    _money_mean: float = 0.0

    @property
    def money_mean(self):
        return self._money_mean

    def _cur_trader_money(self):
        return self.money / self.instr_per_group

    @abstractmethod
    def cur_date_layered(self, df):
        pass


class SingleLayered(LayeredPosition):
    def cur_date_layered(self, df):
        self._instr_per_group = round(len(df) / self.num)
        long = df.loc[:self._instr_per_group - 1, ['type_name_ab']]
        short = df[['type_name_ab']].tail(self._instr_per_group)
        self._money_mean = self._cur_trader_money()
        return long, short


class ManyLayered(LayeredPosition):

    def cur_date_layered(self, df):
        long = pd.DataFrame(columns=['type_name_ab', 'trading_date'])
        short = pd.DataFrame(columns=['type_name_ab', 'trading_date'])
        for name, group in df.groupby('trading_date'):
            group.reset_index(inplace=True)
            self._instr_per_group = round(len(group) / self.num)
            long = pd.concat([long, group.loc[:self._instr_per_group - 1, ['type_name_ab', 'trading_date']]], ignore_index=True)
            short = pd.concat([short, group[['type_name_ab']].tail(self._instr_per_group)], ignore_index=True)
        return long, short


class LayeredBackTestIng(Layered):
    def single_backtesting(self, wc_and_erg, factor_list, periods_list):
        """单进程版本"""
        factor_group_label = list(itertools.product(factor_list, periods_list))
        result = {}
        for factor, holding_od in factor_group_label:
            label_col = f'label_{holding_od}'
            if not result.get(factor):
                result[factor] = {}

            with TimeContext(f'计算单因子-{factor}-{self.num}-{holding_od} cpu'):
                wc_and_erg['trading_date'] = pd.to_datetime(wc_and_erg['trading_date'], unit='s')

                # 1.drop 掉收益率为空的行
                df_no_nan = wc_and_erg.dropna(subset=[label_col, factor])
                # 初始化以交易日为 index，各层为 columns 的 df
                tds = df_no_nan['trading_date'].astype(str).unique().tolist()
                tds = sorted(tds)
                group_return = pd.DataFrame(index=tds, columns=[f'group{i + 1}' for i in range(self.num)])
                group_return.index.rename('trading_date', inplace=True)

                for td in tds:
                    td_df = df_no_nan[df_no_nan['trading_date'] == td]
                    td_df.sort_values(by=[factor, 'wind_code'], ascending=[False, True], inplace=True, ignore_index=True)
                    avg_ret = td_df[label_col].mean()
                    instr_per_group = len(td_df) / self.num

                    for i in range(self.num):
                        group_avg_ret = td_df[label_col].iloc[
                                        round(i * instr_per_group):round((i + 1) * instr_per_group)].mean()
                        group_return.loc[td, f'group{i + 1}'] = group_avg_ret - avg_ret

                # 按持有天数间隔交易日
                tds = group_return.index.tolist()[::holding_od]
                group_return = group_return.loc[tds]

                # 各层超额收益率累加后 +1
                for i in range(self.num):
                    group_return[f'group{i + 1}'] = (group_return[f'group{i + 1}']).cumsum() + 1

            result[factor][label_col] = (group_return['group1'] - group_return['group5']) / 2
        return result

    def celery_backtesting(self, wc_and_erg, factor_list, periods_list):
        """多进程版本"""
        js_df = wc_and_erg.to_json(orient='records', date_unit="s")
        # 6.分层测试
        factor_group_label = list(itertools.product(factor_list, periods_list))
        fgl = Common.list_slice_by_core(factor_group_label)

        result = [celery_backtesting.delay(js_df, f, self.num) for f in fgl]

        temp_df = {}
        with TimeContext(f'分层总时长 cpu'):
            for res in result:
                async_result = AsyncResult(id=str(res), app=app)
                async_result.wait()
                asy_res = async_result.get()
                for key, val in asy_res.items():
                    for k, v in val.items():
                        val[k] = Series(json.loads(v))
                    if not temp_df.get(key):
                        temp_df[key] = val
                    else:
                        temp_df[key].update(val)

                async_result.forget()
        return temp_df
