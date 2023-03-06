from rest_framework import serializers

from apps.monitor.models import CmSecIcIr, CmSeqIcIr


class CmSecICIRSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d', default=None)
    update_time = serializers.DateTimeField(format='%Y-%m-%d', default=None)
    status = serializers.ChoiceField(choices=[(1, "selected"), (0, "not-selected")], source="get_status_display")

    class Meta:
        model = CmSecIcIr
        fields = ['table', 'factor', 'rank_ic', 'rank_ir', 'remark', 'status', 'update_time', 'create_time']


class CmSeqICIRSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d', default=None)
    update_time = serializers.DateTimeField(format='%Y-%m-%d', default=None)
    status = serializers.ChoiceField(choices=[(1, "selected"), (0, "not-selected")], source="get_status_display")

    class Meta:
        model = CmSeqIcIr
        fields = ["type_name_ab",'table', 'factor', 'rank_ic', 'rank_ir', 'remark', 'status', 'update_time', 'create_time']
