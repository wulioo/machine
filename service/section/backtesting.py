import uuid

import pandas as pd

from extra.factory.earnings import FvFactoryEarnings
from service.earnings import Earnings
from service.facotr_base import FvAnalysisBase, FvReviewBase
from service.factor import FutureFactor, EquityFactor
from service.layered import LayeredBackTestIng
from django.core.cache import cache

from service.night import NightTrading


class FactorBackTesting:
    periods: list
    _layered: LayeredBackTestIng
    _earn: Earnings

    def set_layered(self, val):
        self._layered = val

    def set_earn(self, val):
        self._earn = FvFactoryEarnings().make_earnings(self.stime, self.etime, val)

    def layered_backtesting(self, factor_df):
        # 5.计算收益率
        wc_and_erg = self._earn.cal_earnings(factor_df, self.periods)
        # temp_df = self.layered.single_backtesting(wc_and_erg, self.column, self.periods)
        temp_df = self._layered.celery_backtesting(wc_and_erg, self.column, self.periods)

        return self.__responce_backtesting(temp_df)

    def __responce_backtesting(self, temp_df):
        data = {}
        for factor, f_df in temp_df.items():
            result = {l_name: {'x_data': label.tolist(), 'y_data': label.index.tolist()} for l_name, label in
                      f_df.items()}
            data[factor] = self.save_redis(result)
        return data

    def save_redis(self, data):
        """
        分层测试保存数据到redis中
        :param data:
        :return:
        """
        result = {}
        for l_name, label in data.items():
            key_uuid = uuid.uuid1()
            k = f'backtesting-{key_uuid}'
            cache.set(k, label)
            result[l_name] = k
        return result


class FvSecAnalyBackTesting(FvAnalysisBase, FactorBackTesting, NightTrading):
    df = pd.DataFrame()

    def cal_main(self):
        return self.layered_backtesting(self.df)

    def init_data_processing(self):
        factor_df = self.get_fv_factor()
        factor_df = self.get_night_trading_type(factor_df) if self.night else factor_df
        factor_df = self.get_main_contracts(factor_df, self.get_type_name)
        factor_df.dropna(subset=['wind_code'], inplace=True)
        return factor_df


class FvSecReviewBackTesting(FvReviewBase, FactorBackTesting):
    def cal_main(self):
        factor_df = self.init_data_processing()
        return self.layered_backtesting(factor_df)
    def init_data_processing(self):
        factor_df = self.get_main_contracts(self.df, self.get_type_name)
        factor_df.dropna(subset=['wind_code'], inplace=True)
        return factor_df

class EqFactorBackTesting(EquityFactor, FactorBackTesting):
    pass
