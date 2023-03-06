import datetime

from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from apps.monitor.models import CmSecIcIr, CmSeqIcIr
from apps.monitor.serializers import CmSecICIRSerializer, CmSeqICIRSerializer
from extra.db.models_tqfactor import FvFactorInfo
from extra.db.models_tqmain import FutureHeader
from extra.db.models_tqsignal import FvSignalInfo
from extra.factory.earnings import FvFactoryEarnings
from logs import logger
from service.section.icir import FvSecAnalysisICIR, FvSecMonitorICIR
from service.sequential.icir import FvSeqMonitorICIR
from service.varieties import VarietiesAll
from utils.common import Common


# Create your views here.

class MonitorSecICIR(APIView):
    def get(self, request, *args, **kwargs):
        factor = FvSecMonitorICIR()
        result = dict()
        for _db in ['tq_factor', 'tq_signal']:
            factor.set_db(_db)
            for is_night in [False, True]:
                factor.night = is_night
                fv_info = factor.get_info_model.get_info_all(Q(status="live"), ['factor_name', 'table_name'], _db)
                for _t, factor_list in fv_info.groupby(by='table_name'):
                    factor.model = Common.get_models('db', _t)
                    factor.column = factor_list['factor_name'].tolist()
                    factor.df = factor.init_data_processing()
                    result[_t] = factor.cal_main()
        return Response(result, status=status.HTTP_201_CREATED)


class MonitorSeqICIR(APIView):
    def get(self, request, *args, **kwargs):
        factor = FvSeqMonitorICIR()
        result = dict()
        for _db in ['tq_factor']:
            factor.set_db(_db)
            fv_factor_info = factor.get_info_model.get_info_all(Q(status="live"), ['factor_name', 'table_name'], 'tq_factor')
            for _t, factor_list in fv_factor_info.groupby(by='table_name'):
                factor.model = Common.get_models('db', _t)
                factor.column = factor_list['factor_name'].tolist()
                factor.df = factor.init_data_processing()
                result[_t] = factor.cal_main()
        return Response(result, status=status.HTTP_201_CREATED)


class TypeNameAbList(APIView):
    def get(self, request, *args, **kwargs):
        df = FutureHeader.get_duplication_field('type_name_ab', 'tqmain')
        df['exchange'] = df['type_name_ab'].str[-3:]
        type_name_ab = df[df['exchange'].isin(['SHF', 'DCE', 'CZC', 'INE'])]['type_name_ab'].tolist()
        result = []
        for type in type_name_ab:
            result.append({"label": type, "value": type})
        return Response(result, status=status.HTTP_201_CREATED)


class CmSecICIR(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CmSecICIRSerializer

    def get_queryset(self):
        label = self.request.query_params.get('label')
        night = int(self.request.query_params.get('is_night'))
        db = self.request.query_params.get('db')
        return CmSecIcIr.objects.filter(Q(label=label) & Q(is_night=night) & Q(database=db)).all()


class CmSeqICIR(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CmSeqICIRSerializer

    def get_queryset(self):
        label = self.request.query_params.get('label')
        type = self.request.query_params.get('type')
        db = self.request.query_params.get('db')
        return CmSeqIcIr.objects.filter(Q(label=label) & Q(type_name_ab=type) & Q(windows=60) & Q(database=db)).all()
