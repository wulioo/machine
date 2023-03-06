import os
import uuid

import pandas as pd
from matplotlib import pyplot as plt

from Machine.settings import STATICFILES_DIRS
from service.facotr_base import FvAnalysisBase, FvReviewBase
from service.factor import Factor, EquityFactor, FutureFactor
from service.night import NightTrading
from service.sort import SortMixin
from utils.common import Common, TimeContext
from Machine.celery import app
from celery.result import AsyncResult
from apps.future.tasks import celery_box_muster_chart


class FactorDistribute(SortMixin):
    type_name = None

    def celery_box_muster_chart(self, factor_column):
        factor_list = factor_column.drop([self.type_name, 'trading_date'], axis=1).columns.tolist()
        factor_list = Common.list_slice_by_core(factor_list)
        js_df = factor_column.to_json(orient='records', date_unit="s")

        result = [celery_box_muster_chart.delay(js_df, factor, self.type_name) for factor in factor_list]
        factor_dict = {}
        for res in result:
            async_result = AsyncResult(id=str(res), app=app)
            async_result.wait()
            factor_dict.update(async_result.get())
            async_result.forget()

        return factor_dict

    def single_box_muster_chart(self, factor_column):
        """单进程版本"""
        factor_list = factor_column.drop([self.type_name, 'trading_date'], axis=1).columns.tolist()
        f_list = {}
        for x in factor_list:
            with TimeContext(f'{x}-画盒须图 io'):
                x_df = factor_column[['trading_date', self.type_name, x]]
                x_df.dropna(subset=x, inplace=True)
                x_df1 = x_df.pivot(index='trading_date', columns=self.type_name).reset_index(drop=True)
                x_df1.columns = [i[1] for i in x_df1.columns]
                x_df1.boxplot(figsize=(24, 8), grid=False, showmeans=True, rot=30)
                plt.title(f'{x} distribution per type', size=15)
                plt.grid(True, alpha=.5, ls='--')
                key_uuid = uuid.uuid1()
                file_name = os.path.join(STATICFILES_DIRS[0], f'images/{key_uuid}.png')
                plt.savefig(file_name, bbox_inches='tight')
                plt.close()
            f_list[x] = f'static/images/{key_uuid}.png'
        return f_list

    def box_chart_factor_sort(self, df):
        factor_list = self.column
        # df.dropna(subset=self.column, inplace=True)
        factor_arr = self.get_factor_sort(df)
        df = factor_arr.drop(columns=factor_list)
        f_sort_list = df.drop([self.type_name, 'trading_date'], axis=1).columns.tolist()
        mean_df = df.groupby('trading_date').mean()
        mean_df = mean_df.reset_index(col_fill='trading_date')
        df = df.merge(mean_df, how='left', on='trading_date')
        factor_x = [f'{x}_x' for x in f_sort_list]
        factor_y = [f'{y}_y' for y in f_sort_list]
        df[f_sort_list] = df[factor_x].values - df[factor_y].values
        df = df[f_sort_list + ['trading_date', self.type_name]]
        return df


class FvSecAnalyDistribute(FvAnalysisBase, FactorDistribute, NightTrading):
    df = pd.DataFrame()
    type_name = 'type_name_ab'

    def cal_main(self):
        df = self.df.drop(['wind_code'], axis=1)
        return self.celery_box_muster_chart(df)

    def init_data_processing(self):
        factor_df = self.get_fv_factor()
        factor_df = self.get_night_trading_type(factor_df) if self.night else factor_df
        factor_df = self.box_chart_factor_sort(factor_df) if self.sort else factor_df
        factor_df['wind_code'] = 'test'
        return factor_df


class FvSecReviewDistribute(FvReviewBase, FactorDistribute):
    type_name = 'type_name_ab'
    def cal_main(self):
        return self.celery_box_muster_chart(self.df)

    def init_data_processing(self):
        pass


class EqFactorDistribute(EquityFactor, FactorDistribute):
    type_name = 'wind_code'
