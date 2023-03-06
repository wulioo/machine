from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
from apps.api_fv_sequential.serializers import FvSqICSerializer, FvSqRankICSerializer
from extra.db.models_tqfactor import FvFactorInfo
from extra.factory.earnings import FvFactoryEarnings
from extra.factory.table_name import TableTypeFactory
from service.sequential.icir import FvSeqAnalysisICIR, FvSeqApiICIR
from service.table_name import Table
from service.table_type import FactorSingleTable
# from service.table_type import SingleTable

from service.varieties import VarietiesFactory, VarietiesAll
from utils.common import Common


class FvSqApiList(APIView):
    def get(self, request, *args, **kwargs):
        type_name_ab = request.query_params['type_name_ab']

        factor_df = FvFactorInfo.get_info_all(Q(status='live'), ['factor_name', 'table_name'], 'tq_factor')
        table_name = factor_df.drop_duplicates(subset=['table_name'], keep='first')['table_name']
        result = []
        for table in table_name:
            model = Common.get_models('db', table)
            factor_col = model.get_info_all(Q(type_name_ab=type_name_ab), factor_df.loc[factor_df['table_name'] == table, 'factor_name'].to_list(), 'tq_factor').isnull().all()
            factor_col = factor_col[factor_col == False].index
            if not factor_col.empty:
                result += factor_col.to_list()
        return Response(result, status=status.HTTP_201_CREATED)


class FvSqCalIC(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
      时序期货 分类
      计算ICIR1
      """
    serializer_class = FvSqICSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stime = serializer.data['stime']
        etime = serializer.data['etime']
        factor = FvSeqAnalysisICIR()
        factor.etime = etime
        factor.vari = VarietiesFactory.create_varieties(serializer.data['varieties'])
        factor.earn = FvFactoryEarnings().make_earnings(stime, etime, serializer.data['earnings_fun'])
        factor.windows = serializer.data['windows']  # 时间窗口
        factor.correlation = serializer.data['correlation']  # 相关系数
        factor.periods = serializer.data['periods']  # 收益周期
        factor.exchange = serializer.data['exchange_future']  # 交易所
        factor.interval = serializer.data['interval']  # 间隔
        factor.stime = Common.get_previous_interval_trading_time(stime, factor.interval)

        result = {}
        for table, factor_list in serializer.data['factor'].items():
            factor.model = Common.get_models('db', table)
            factor.column = factor_list  # 因子
            factor.df = factor.init_data_processing()
            data = factor.cal_main()
            result[table] = factor.resp_api_data(data)

        return Response(result, status=status.HTTP_201_CREATED)


class FvSqCalRankICIR(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
      时序期货 分类
      计算ICIR1
      """
    serializer_class = FvSqRankICSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stime = serializer.data['stime']
        etime = serializer.data['etime']
        factor = FvSeqApiICIR(serializer.data['type_name_ab'])
        factor.etime = etime
        factor.vari = VarietiesAll()
        factor.earn = FvFactoryEarnings().make_earnings(stime, etime, serializer.data['earnings_fun'])
        factor.windows = serializer.data['windows']  # 时间窗口
        factor.correlation = serializer.data['correlation']  # 相关系数
        factor.periods = serializer.data['periods']  # 收益周期
        factor.stime = Common.get_previous_interval_trading_time(stime, factor.interval)
        factor_service = FactorSingleTable(factor)
        result = factor_service.main(serializer.data['factor'])

        return Response(result, status=status.HTTP_201_CREATED)
