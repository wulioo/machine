from abc import abstractmethod

import pandas as pd
from django.db.models import Sum, Q

from apps.equity.models import EquityDailyType
from apps.future.models import FutureDailyType
from logs import logger
from service.facotr_base import FvAnalysisBase
from service.factor import FutureFactor, EquityFactor
from service.night import NightTrading
from utils.exception import CommonException


class FactorAvgVarie:
    type_name = None

    def cal_coverage(self, table_df: pd.DataFrame):
        table_df.drop(columns=[self.type_name], inplace=True)
        factor_count = table_df.groupby('trading_date').count()
        factor_count.reset_index(level=0, inplace=True)
        trading_type_count = self.get_trader_type()
        try:
            type_df = factor_count.merge(trading_type_count, how='left', on='trading_date')
        except Exception as e:
            logger.error('future_daily_type表为空')
            raise CommonException(400, f"future_daily_type表为空")
        factor_col = type_df.drop(columns=['trading_date', 'total']).columns.tolist()
        coverage = type_df[factor_col].div(type_df['total'], axis=0).mean()
        coverage = pd.DataFrame(coverage)
        coverage['count'] = type_df.iloc[-1][factor_col]
        coverage['total'] = type_df.iloc[-1]['total']

        coverage = coverage.reset_index()
        coverage.columns = ['factor', 'coverage', 'count', 'total']
        coverage['coverage'] = (coverage['coverage'] * 100).round(2).astype(str) + '%'
        return coverage

    @abstractmethod
    def get_trader_type(self):
        pass


class FvSecAnalyAvgVarie(FvAnalysisBase, FactorAvgVarie, NightTrading):
    df = pd.DataFrame()
    type_name = 'type_name_ab'

    def cal_main(self):
        return self.cal_coverage(self.df)

    def init_data_processing(self):
        factor_df = self.get_fv_factor()
        factor_df = self.get_night_trading_type(factor_df) if self.night else factor_df
        return factor_df

    def get_trader_type(self):
        trading_type_count = FutureDailyType.objects \
            .filter(Q(trading_date__range=[self.stime, self.etime]) & Q(exchange__in=self.exchange)) \
            .values('trading_date') \
            .annotate(total=Sum('total'))
        return pd.DataFrame(trading_type_count)


class FvFactorAvgVarie(FutureFactor, FactorAvgVarie, NightTrading):
    type_name = 'type_name_ab'

    def get_trader_type(self):
        trading_type_count = FutureDailyType.objects \
            .filter(Q(trading_date__range=[self.stime, self.etime]) & Q(exchange__in=self.exchange)) \
            .values('trading_date') \
            .annotate(total=Sum('total'))
        return pd.DataFrame(trading_type_count)


class EqFactorAvgVarie(EquityFactor, FactorAvgVarie):
    type_name = 'wind_code'

    def get_trader_type(self):
        trading_type_count = EquityDailyType.objects \
            .filter(Q(trading_date__range=[self.stime, self.etime]) & Q(index_code=self.index_code)) \
            .values('trading_date', 'total')
        return pd.DataFrame(trading_type_count)
