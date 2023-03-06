import json

import pandas as pd

from service.axis import AxisMixin
from service.earnings import Earnings
from service.facotr_base import FvAnalysisBase, FvReviewBase
from service.factor import FutureFactor, EquityFactor
from service.night import NightTrading
from service.varieties import Varieties
import itertools

from utils.common import Common
from apps.future.tasks import celery_ndcg
from celery.result import AsyncResult
from Machine.celery import app


class FactorNdcg(AxisMixin):
    periods = None
    vari: Varieties
    earn: Earnings

    def cal_ndcg(self, df):
        # 计算收益率
        wc_and_erg = self.earn.cal_earnings(df, self.periods)
        # 计算ndcg
        self.get_y_x_xy(wc_and_erg, self.column, self.periods)
        result = self.__celery_ndcg(wc_and_erg)
        return self.__responce_ndcg(result)

    def __celery_ndcg(self, df):
        """计算cal ndcg"""
        factor_label = list(itertools.product(self.ys, self.xs))
        fl_list = Common.list_slice_by_core(factor_label)

        js_df = df.to_json(orient='records', date_unit="s")
        result = [celery_ndcg.delay(js_df, fl) for fl in fl_list]
        temp_data = {}
        for res in result:
            async_result = AsyncResult(id=str(res), app=app)
            async_result.wait()

            for key, list_val in async_result.get().items():

                list_df = [pd.read_json(df, encoding="utf-8", orient='records') for df in list_val]
                if isinstance(temp_data.get(key), pd.DataFrame):
                    sign_df = pd.concat(list_df)
                    temp_data[key] = pd.concat([temp_data[key], sign_df])
                else:
                    temp_data[key] = pd.concat(list_df)

            async_result.forget()  # 将结果删除,执行完成，结果不会自动删除

        return temp_data

    def __responce_ndcg(self, data):
        result = dict()
        for key, val in data.items():
            val.index.rename('factor', inplace=True)
            res = val.reset_index()
            res = res.T.to_json()
            res = list(json.loads(res).values())
            result[key] = res
        return result


class FvSecAnalyNdcg(FvAnalysisBase, FactorNdcg, NightTrading):
    df: pd.DataFrame

    def cal_main(self):
        return self.cal_ndcg(self.df)

    def init_data_processing(self):
        factor_df = self.get_fv_factor()
        factor_df = self.get_night_trading_type(factor_df) if self.night else factor_df
        factor_df = self.vari.fill_df_value(factor_df, self.column)
        factor_df = self.get_main_contracts(factor_df, self.get_type_name)
        factor_df.dropna(subset=['wind_code'], inplace=True)
        return factor_df


class FvSecReviewNdcg(FvReviewBase, FactorNdcg):
    def cal_main(self):
        df = self.init_data_processing()
        return self.cal_ndcg(df)

    def init_data_processing(self):
        factor_df = self.get_main_contracts(self.df, self.get_type_name)
        factor_df.dropna(subset=['wind_code'], inplace=True)
        return factor_df


class EqFactorNdcg(EquityFactor, FactorNdcg):
    pass
