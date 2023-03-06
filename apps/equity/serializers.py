from rest_framework import serializers

from apps.future.serializers import FactorMinxin, TimeMinxin, ICIRMinxin, TableNameMinxin, FactorSortMinxin, PerEarningsMinxin, IndexCodeMixin, CorrMinxin, RedisKeyMinxin, \
    LayeredNumMinxin, TimeTableFactorMinxin, FactorNDCGReviewSerializer, SingleLayeringMinxin, EarningsFunMinxin
from utils.code import StatusCode
from utils.exception import CommonException


# -----------------------股票-------------------------- #

class FactorEquityIcIrSerializer(FactorMinxin, TimeMinxin, IndexCodeMixin, FactorSortMinxin, PerEarningsMinxin,
                                 RedisKeyMinxin, CorrMinxin):
    factor_diff = serializers.ListField(required=True)


class FactorEqZonalTestingSerializer(FactorMinxin, TimeMinxin, LayeredNumMinxin, IndexCodeMixin, PerEarningsMinxin,
                                     RedisKeyMinxin):
    pass


class FactorEqCorrSerializer(TimeMinxin, FactorMinxin, FactorSortMinxin):
    pass


class FactorEqNdcgSerializer(FactorMinxin, TimeMinxin, PerEarningsMinxin, IndexCodeMixin):
    pass


class FactorEqBacktestingSerializer(TimeMinxin, FactorMinxin, SingleLayeringMinxin, PerEarningsMinxin,IndexCodeMixin):
    pass

class FactorEqVarieAvgSerializer(TimeMinxin, FactorMinxin, IndexCodeMixin, ):
    pass
# class FactorEqDistributeReviwSerializer(TimeTableFactorMinxin):
#     pass

class FactorEqReviewSerializer(CorrMinxin, FactorSortMinxin, PerEarningsMinxin, RedisKeyMinxin):
    factor_diff = serializers.ListField(required=True)

    def validate_correlation(self, value):
        if not value[0]:
            raise CommonException(400, '请选择相关系数')
        return value[0].split(',')

    def validate_periods(self, value):
        if not value[0]:
            raise CommonException(400, '请选择收益周期')
        val_list = value[0].split(',')
        return [int(val) for val in val_list]

    def validate_factor_diff(self, value):
        if value[0]:
            val_list = value[0].split(',')
            return [val for val in val_list]
        return []


class FactorEqDistributeSerializer(TimeMinxin, FactorMinxin, FactorSortMinxin, IndexCodeMixin):
    pass


class FactorEqLayeredReviewSerializer(PerEarningsMinxin, LayeredNumMinxin, RedisKeyMinxin):
    factor_neu = serializers.BooleanField(required=True)

    def validate_layered_num(self, value):
        if not value[0]:
            raise CommonException(400, '请选择分层层数')
        val_list = value[0].split(',')
        return [int(val) for val in val_list]

    def validate_periods(self, value):
        if not value[0]:
            raise CommonException(400, '请选择收益周期')
        val_list = value[0].split(',')
        return [int(val) for val in val_list]
