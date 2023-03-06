from rest_framework import serializers

from apps.future.serializers import FactorMinxin, TimeMinxin, ICIRMinxin, TableNameMinxin
from utils.code import StatusCode
from utils.exception import CommonException

class FacorMixin(serializers.Serializer):
    interval = serializers.IntegerField(required=True)

# class FvNormalICSerializer(FactorMinxin, TimeMinxin, ICIRMinxin,TableNameMinxin,IntervalMinxin):
#     earnings_fun = serializers.CharField(required=True, max_length=50)
#     varieties = serializers.CharField(required=True, max_length=50)
#     windows = serializers.ListField(required=True, max_length=50)
#
#     def validate_factor(self, value):
#         if not value:
#             raise CommonException(StatusCode.ERROR.code, f"请选择因子表!")
#         return value
#
