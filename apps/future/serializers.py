# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.serializers import Serializer

from extra.db.models_tqfactor import FutureTechDailyFactor
from extra.db.models_tqmain import FutureDaily
from utils.code import StatusCode
from utils.exception import CommonException


class ExchangeMixin(Serializer):
    """交易所"""
    exchange_future = serializers.ListField(required=True, max_length=11, min_length=1)


class IndexCodeMixin(Serializer):
    """指数选择"""
    index_code = serializers.CharField(max_length=50, allow_blank=True)


class CorrMinxin(Serializer):
    """
    相关性：correlation
    """
    correlation = serializers.ListField(required=True, max_length=11, min_length=1)


class PeriodsMinxin(Serializer):
    """收益周期：periods"""
    periods = serializers.ListField(required=True, max_length=11, min_length=1,
                                    error_messages={'min_length': '收益周期至少有一个元素'})


class FactorDiffMinxin(Serializer):
    """平均因子收益"""
    factor_diff = serializers.BooleanField(required=True)


class FactorSortMinxin(Serializer):
    """因子排序"""
    factor_sort = serializers.BooleanField(required=True)


class WeightMinxin(Serializer):
    """因子权重"""
    weight = serializers.DictField()


class SingleTimeMinxin(Serializer):
    """今天时间"""
    cur_time = serializers.DateTimeField(format='%Y-%m-%d', default=None)

    def validate_cur_time(self, value):
        if not value:
            raise CommonException(StatusCode.ERROR.code, f"缺少cur_time时间！")
        return value


class TableNameMinxin(Serializer):
    table_name = serializers.CharField(required=True, max_length=20, min_length=1)


class TypeNameMinxin(Serializer):
    """品种标的"""
    type_name_ab = serializers.ListField(required=True)

    def validate_type_name_ab(self, value):
        return [val.upper() for val in value]


class SinglePeriodsMinxin(Serializer):
    """单个收益周期"""
    periods = serializers.IntegerField(required=True)


class SingleLayeringMinxin(Serializer):
    """单个分层层数"""
    layering = serializers.IntegerField(required=True)


class MoneyMinxin(Serializer):
    money = serializers.IntegerField(required=True)


class TimeMinxin(Serializer):
    stime = serializers.DateTimeField(format='%Y-%m-%d', default=None)
    etime = serializers.DateTimeField(format='%Y-%m-%d', default=None)

    def validate_stime(self, value):
        if not value:
            raise CommonException(StatusCode.ERROR.code, f"缺少start_time时间！")
        return value

    def validate_etime(self, value):
        if not value:
            raise CommonException(StatusCode.ERROR.code, f"缺少end_time时间！")
        return value

    def validate(self, attrs):
        stime = attrs['stime']
        etime = attrs['etime']
        diff_day = etime - stime
        if diff_day.days < 10:
            raise CommonException(StatusCode.ERROR.code, f"时间窗口太短！")
        return attrs


class FactorMinxin(Serializer):
    factor = serializers.DictField()

    def validate_factor(self, value):
        if not value:
            raise CommonException(StatusCode.ERROR.code, f"请选择因子表!")
        return value


class RedisKeyMinxin(Serializer):
    redis_key = serializers.CharField(max_length=60)


class EarningsFunMinxin(Serializer):
    """收益方法"""
    earnings_fun = serializers.CharField(required=True, max_length=20, min_length=1)


class VarietiesMinxin(Serializer):
    """标的选择"""
    varieties = serializers.CharField(required=True, max_length=20, min_length=1)


class LayeredNumMinxin(Serializer):
    layered_num = serializers.ListField(required=True, max_length=10, min_length=1)


class LayeredFunMinxin(Serializer):
    layered_fun = serializers.ListField(required=True, max_length=10, min_length=1)


class PlatformMinxin(Serializer):
    platform = serializers.IntegerField(required=True)


class TableTypeMinxin(Serializer):
    table_type = serializers.CharField(required=True)


class FactorSingleMinxin(Serializer):
    factor = serializers.CharField(required=True, max_length=50)


class NightTradingMinxin(Serializer):
    night_trading = serializers.BooleanField(required=True)


# ------------------------------组合方法----------------------------- #
class TimeTableFactorMinxin(TimeMinxin, FactorMinxin, TableNameMinxin, NightTradingMinxin):
    """时间，因子，表类型,夜盘交易"""
    pass


class LayeredMinxin(LayeredNumMinxin, LayeredFunMinxin):
    """分层方法，分层层数"""
    pass


class EarVarietieMinxin(EarningsFunMinxin, VarietiesMinxin):
    """收益方法，标的选择"""
    pass


class ICIRMinxin(ExchangeMixin, CorrMinxin, PeriodsMinxin):
    """
    交易所,相关性,收益周期
    """
    pass


class CalSelectMinxin(FactorDiffMinxin, FactorSortMinxin):
    """
    因子差异对比
    因子排序
    """
    pass


class PerExchangMinxin(PeriodsMinxin, ExchangeMixin):
    """
    收益周期,交易所
    """
    pass


class PerEarningsMinxin(PeriodsMinxin, EarningsFunMinxin):
    """
    收益周期,收益方法
    """
    pass


class FactorTableMinxin(FactorSingleMinxin, TableNameMinxin):
    pass


# ------------------------------序列器------------------------------ #
class FactorIcIrSerializer(TimeTableFactorMinxin, ICIRMinxin, CalSelectMinxin, EarVarietieMinxin):
    pass


class FactorZonalTestingSerializer(TimeTableFactorMinxin, PerExchangMinxin, LayeredMinxin, EarVarietieMinxin,
                                   RedisKeyMinxin):
    pass


class FactorPositioningSerializer(FactorMinxin, TableNameMinxin, SingleTimeMinxin, TypeNameMinxin, SinglePeriodsMinxin,
                                  SingleLayeringMinxin, NightTradingMinxin, WeightMinxin, MoneyMinxin):
    pass


class FactorBacktestingSerializer(TimeTableFactorMinxin, SingleLayeringMinxin, EarningsFunMinxin, PerExchangMinxin):
    pass


class FactorNdcgSerializer(TimeTableFactorMinxin, PerExchangMinxin, EarVarietieMinxin):
    pass


class FactorCorrSerializer(TimeTableFactorMinxin, FactorSortMinxin, PlatformMinxin):
    pass


class FactorDistributeSerializer(TimeTableFactorMinxin, FactorSortMinxin, ExchangeMixin):
    pass


class FactorBacktestingReviewSerializer(SingleLayeringMinxin, PerEarningsMinxin):
    def validate_periods(self, value):
        if not value[0]:
            raise CommonException(400, '请选择收益周期')
        val_list = value[0].split(',')
        return [int(val) for val in val_list]


class FactorNDCGReviewSerializer(PerEarningsMinxin):

    def validate_periods(self, value):
        if not value[0]:
            raise CommonException(400, '请选择收益周期')
        val_list = value[0].split(',')
        return [int(val) for val in val_list]


class FactorLayeredReviewSerializer(FactorNDCGReviewSerializer, LayeredNumMinxin, RedisKeyMinxin):
    def validate_layered_num(self, value):
        if not value[0]:
            raise CommonException(400, '请选择分层层数')
        val_list = value[0].split(',')
        return [int(val) for val in val_list]


class FactorReviewSerializer(FactorNDCGReviewSerializer, CalSelectMinxin, CorrMinxin):

    def validate_correlation(self, value):
        if not value[0]:
            raise CommonException(400, '请选择相关系数')
        return value[0].split(',')

class FactorCacheICSerializer(RedisKeyMinxin):
    table_name = serializers.CharField(required=True, max_length=50)
    correlation = serializers.CharField(required=True, max_length=20)
    corr_label = serializers.CharField(required=True, max_length=20)


class FactorCacheEchartsSerializer(RedisKeyMinxin):
    table_name = serializers.CharField(required=True, max_length=50)
    factor = serializers.CharField(required=True, max_length=50)
    group_name = serializers.CharField(required=True, max_length=20)
    factor_label = serializers.CharField(required=True, max_length=20)





class FactorFvEarnings(TimeMinxin, PerExchangMinxin, EarningsFunMinxin):
    pass


class FactorFvSharpeEarnings(FactorFvEarnings):

    def validate_periods(self, value):
        if min(value) <= 1:
            raise CommonException(400, '收益周期最小为2')

        return value


class FactorVarieAvgSerializer(TimeTableFactorMinxin, ExchangeMixin, ):
    pass


