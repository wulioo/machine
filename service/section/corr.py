import pandas as pd
from django.db.models import Q

from service.facotr_base import FvAnalysisBase, FvReviewBase
from service.factor import FutureFactor, EquityFactor
from service.night import NightTrading
from service.sort import SortMixin
from utils.exception import ResultEmpty


class SectionCorr(SortMixin):
    type_name: str

    def cal_corr(self, df: pd.DataFrame):
        return df.corr().fillna(0)


class FvSecAnalysisCorr(FvAnalysisBase, SectionCorr, NightTrading):
    type_name = 'type_name_ab'
    df: pd.DataFrame

    def get_fv_factor(self):
        df = self.model.get_orderby_info_all(Q(trading_date__range=[self.stime, self.etime]),
                                             self.column + ['trading_date', self.type_name],
                                             [self.type_name, 'trading_date'], self._db)
        if df.empty:
            raise ResultEmpty(400, msg=f'{self.model._meta.db_table} 获取数据为空')
        return df

    def init_data_processing(self):
        factor_df = self.get_fv_factor()
        factor_df = self.get_night_trading_type(factor_df) if self.night else factor_df
        factor_df = self.get_factor_sort(factor_df) if self.sort else factor_df
        return factor_df

    def cal_main(self):
        return self.cal_corr(self.df)


class FvSecReviewCorr(FvReviewBase, SectionCorr):
    type_name = 'type_name_ab'
    model = None
    _db: str

    def set_db(self, val):
        self._db = val

    def __init__(self, file_df: pd.DataFrame):
        self.file_df = file_df
        self.file_cols = file_df.drop(labels=['trading_date', 'type_name_ab'], axis=1).columns.tolist()
        FvReviewBase.__init__(self, file_df)

    def get_fv_factor(self):
        df = self.model.get_orderby_info_all(Q(trading_date__range=[self.stime, self.etime]),
                                             self.column + ['trading_date', self.type_name],
                                             [self.type_name, 'trading_date'], self._db)
        if df.empty:
            raise ResultEmpty(400, msg=f'{self.model._meta.db_table} 获取数据为空')
        return df

    def init_data_processing(self):
        factor_df = self.get_fv_factor()
        factor_df = self.get_factor_sort(factor_df) if self.sort == 'true' else factor_df
        return factor_df

    def cal_main(self):
        self.column = self.file_cols
        file_df = self.get_factor_sort(self.file_df) if self.sort == 'true' else self.file_df
        factor_merge = file_df.merge(self.df, how="outer", on=['trading_date', 'type_name_ab'])
        result = self.cal_corr(factor_merge)
        return result[self.column]
