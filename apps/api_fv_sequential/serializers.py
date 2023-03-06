from rest_framework import serializers

from apps.future.serializers import FactorMinxin, TimeMinxin, ICIRMinxin, TableNameMinxin, EarningsFunMinxin, VarietiesMinxin, CorrMinxin, PeriodsMinxin
from apps.fv_sequential.serializers import IntervalMinxin, WindowsMixin
from utils.code import StatusCode
from utils.exception import CommonException


class TypeNameAbMixin(serializers.Serializer):
    type_name_ab = serializers.CharField(required=True)


class WindowsSingleMixin(serializers.Serializer):
    windows = serializers.IntegerField(required=True)


class FactorListMixin(serializers.Serializer):
    factor = serializers.ListField(required=True, max_length=300)


class PeriodsSingleMinxin(serializers.Serializer):
    periods = serializers.IntegerField(required=True)


class ThresholdMixin(serializers.Serializer):
    threshold = serializers.FloatField(required=True)


class FvSqICSerializer(FactorMinxin, TimeMinxin, ICIRMinxin, IntervalMinxin, WindowsMixin, EarningsFunMinxin, VarietiesMinxin):
    pass


class FvSqRankICSerializer(FactorMinxin, TypeNameAbMixin, TimeMinxin, PeriodsMinxin,CorrMinxin, WindowsMixin, EarningsFunMinxin,IntervalMinxin):
    pass
