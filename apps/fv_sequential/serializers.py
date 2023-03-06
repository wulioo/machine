from rest_framework import serializers

from apps.future.serializers import FactorMinxin, TimeMinxin, ICIRMinxin, TableNameMinxin, VarietiesMinxin, EarningsFunMinxin, FactorSortMinxin
from utils.code import StatusCode
from utils.exception import CommonException


class IntervalMinxin(serializers.Serializer):
    interval = serializers.IntegerField(required=True)


class WindowsMixin(serializers.Serializer):
    windows = serializers.ListField(required=True, max_length=50)


class FvIcIrSerializer(FactorMinxin, TimeMinxin, ICIRMinxin, TableNameMinxin, IntervalMinxin, WindowsMixin, EarningsFunMinxin, VarietiesMinxin):

    def validate_factor(self, value):
        if not value:
            raise CommonException(StatusCode.ERROR.code, f"请选择因子表!")
        return value


class FvIcIrRedisSerializer(serializers.Serializer):
    table_type = serializers.CharField(max_length=50, required=True, error_messages={'blank': "当前标的没有主力合约"})
    corr_label = serializers.CharField(max_length=22, required=True)
    windows = serializers.CharField(max_length=22, required=True)
    corr = serializers.CharField(max_length=22, required=True)


class FvICIRReviewSerializer(serializers.Serializer):
    correlation = serializers.ListField(required=True, max_length=10, min_length=1)
    periods_list = serializers.ListField(required=True, max_length=10, min_length=1)
    earnings_fun = serializers.CharField(required=True, max_length=50)
    windows = serializers.ListField(required=True, max_length=50)

    def validate_correlation(self, value):
        if not value[0]:
            raise CommonException(400, '请选择相关系数')
        return value[0].split(',')

    def validate_windows(self, value):
        if not value[0]:
            raise CommonException(400, '请选择时间窗口')
        val_list = value[0].split(',')
        return [int(val) if val != 'till_now' else val for val in val_list]

    def validate_periods_list(self, value):
        if not value[0]:
            raise CommonException(400, '请选择收益周期')
        val_list = value[0].split(',')
        return [int(val) for val in val_list]


class FvCorrSerializer(TimeMinxin, FactorMinxin, TableNameMinxin, FactorSortMinxin):
    pass
