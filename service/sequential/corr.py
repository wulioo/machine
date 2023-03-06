import pandas as pd
from django.db.models import Q

from service.facotr_base import FvAnalysisBase
from service.sort import SortMixin
from utils.exception import ResultEmpty


class SequentialCorr(SortMixin):
    type_name: str

    def cal_corr(self, df: pd.DataFrame):
        type_list = df['type_name_ab'].drop_duplicates(keep='first')
        corr_df = df.groupby(self.type_name).corr().fillna(0)
        result = {t: corr_df.loc[t] for t in type_list}
        return result


class FvSeqAnalysisCorr(FvAnalysisBase, SequentialCorr):
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
        factor_df = self.get_factor_sort(factor_df) if self.sort else factor_df
        return factor_df

    def cal_main(self):
        return self.cal_corr(self.df)
