import pandas as pd

from utils.common import TimeContext


class SortMixin:
    sort = None
    column = None

    def get_factor_sort(self, df: pd.DataFrame):
        """
        因子排名
        :return:
        """
        with TimeContext('因子排名计算 cpu'):
            rank_cols = [f'{col}_rank' for col in df if col in self.column]
            df[rank_cols] = df[['trading_date'] + self.column].round(8).groupby('trading_date').rank()
            self.column = self.column + rank_cols
        return df
