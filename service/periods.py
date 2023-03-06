from abc import ABCMeta, abstractmethod

import pandas as pd
from django.db.models import Q

from extra.db.models_tqmain import TradingDateInfo, FutureHeader, FutureDaily, FutureDominantDaily
from typing import Optional

from utils.exception import ResultEmpty


class Periods(metaclass=ABCMeta):

    def __init__(self):
        self.label = None


class PositioningPeriods(Periods):
    _db: str

    @abstractmethod
    def get_factor(self, factor):
        pass

    def set_db(self, val):
        self._db = val


class SinglePeriods(PositioningPeriods):

    def get_factor(self, factor) -> pd.DataFrame:
        df = factor.model.get_info_all(Q(trading_date=factor.stime), [factor.column] + ['type_name_ab', 'trading_date'], self._db)
        if df.empty:
            raise ResultEmpty(msg=f'{factor.model._meta.db_table} Result Is None')
        df.sort_values(by=factor.column, ascending=False, inplace=True, ignore_index=True)
        factor_df = factor.get_night_trading_type(df) if factor.night else df
        return factor_df


class ManyPeriods(PositioningPeriods):

    def get_factor(self, factor) -> pd.DataFrame:
        trading_date = TradingDateInfo.get_info_all(Q(nature_date__lte=factor.stime) & Q(is_trading_date=1), ['nature_date'], 'tqmain')
        trading_date = list(trading_date['nature_date'].unique())[-self.label:]
        df = factor.model.get_info_all(Q(trading_date__in=trading_date), [factor.column] + ['type_name_ab', 'trading_date'], self._db)
        if df.empty:
            raise ResultEmpty(msg=f'{factor.model._meta.db_table} Result Is None')
        df.sort_values(by=['trading_date', factor.column], ascending=[False, False], inplace=True, ignore_index=True)
        return df
