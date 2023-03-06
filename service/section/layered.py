from abc import ABC

import pandas as pd

from service.earnings import Earnings
from service.facotr_base import FvAnalysisBase, FvReviewBase
from service.factor import Factor, EquityFactor, FutureFactor
from service.layered import LayeredTest
from django.core.cache import cache

from service.night import NightTrading
from service.varieties import VarietiesFactory


class FactorLayered:
    periods = None
    _vari = None
    _layered: LayeredTest
    _earn: Earnings

    def set_layered(self, val):
        self._layered = val

    def set_earn(self, val):
        self._earn = val

    def set_vari(self, val):
        self._vari = VarietiesFactory.create_varieties(val)  # 标的方法

    def layered_test(self, factor_arr):
        # 5.计算收益率
        wc_and_erg = self._earn.cal_earnings(factor_arr, self.periods)
        return self._layered.celyer_group_cumsum(wc_and_erg, self.column, self.periods)

    def resp_layered(self, temp_df, table, redis_key):
        data = {}
        for factor, f_df in temp_df.items():
            data[factor] = {}
            for group, g_df in f_df.items():
                tmp_res = {l_name: '' for l_name, label in g_df.items()}
                data[factor][f'group{group}'] = tmp_res
                result = {l_name: label for l_name, label in g_df.items()}
                self.save_redis(result, factor, f'group{group}', table, redis_key)
        return data

    def save_redis(self, data, factor, n_group, table, redis_key):
        """
        分层测试保存数据到redis中
        :param data:
        :param table:
        :param factor:
        :param n_group:
        :param redis_key:
        :return:
        """
        for l_name, label in data.items():
            k = f'{table}-{factor}-{n_group}-{l_name}-{redis_key}'
            cache.set(k, label)


class FvSecAnalyLayered(FvAnalysisBase, FactorLayered, NightTrading):
    df: pd.DataFrame
    table: str
    redis_key: str

    def init_data_processing(self):
        factor_df = self.get_fv_factor()
        factor_df = self.get_night_trading_type(factor_df) if self.night else factor_df
        factor_df = self._vari.fill_df_value(factor_df, self.column)
        factor_df = self.get_main_contracts(factor_df, self.get_type_name)
        factor_df.dropna(subset=['wind_code'], inplace=True)
        return factor_df

    def cal_main(self):
        return self.layered_test(self.df)


class FvSecOneReviewLayered(FvReviewBase, FactorLayered):
    def cal_main(self):
        df = self.init_data_processing()
        return self.layered_test(df)

    def init_data_processing(self):
        factor_df = self.get_main_contracts(self.df, self.get_type_name)
        factor_df.dropna(subset=['wind_code'], inplace=True)
        return factor_df


class FvSecTwoReviewLayered(FvReviewBase, FactorLayered):
    def __init__(self, file_df: pd.DataFrame, file_price: pd.DataFrame):
        self.file_price = file_price
        super(FvSecTwoReviewLayered, self).__init__(file_df)

    def cal_main(self):
        wc_and_erg = self._earn.cal_file_earnings(self.df, self.file_price, self.periods)
        temp_df = self._layered.celyer_group_cumsum(wc_and_erg, self.column, self.periods)
        return temp_df
    def init_data_processing(self):
        pass


class EqLayeredFactor(EquityFactor, FactorLayered):
    pass
