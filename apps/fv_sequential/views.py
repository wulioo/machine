import numpy as np
from django.core.cache import cache
from django.shortcuts import render
import json
# Create your views here.
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from apps.future.serializers import FactorCorrSerializer
from apps.fv_sequential.serializers import FvIcIrSerializer, FvIcIrRedisSerializer, FvICIRReviewSerializer, FvCorrSerializer
from extra.factory.earnings import FvFactoryEarnings
from extra.factory.table_name import  TableTypeFactory
from service.earnings import FutureEarnings
from service.file import File
from service.sequential.corr import FvSeqAnalysisCorr
from service.sequential.icir import FvSeqAnalysisICIR, FvSeqReviewICIR
from service.varieties import Varieties, VarietiesFactory
from utils.common import Common, TimeContext
from utils.exception import CommonException


class FvCalIcIr(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
      时序期货 分类
      计算ICIR1
      """
    serializer_class = FvIcIrSerializer

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
        factor_service = TableTypeFactory.make_table(serializer.data['table_name'], factor)
        result = factor_service.main(serializer.data['factor'])
        return Response(result, status=status.HTTP_201_CREATED)


class FvICIRReview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """期货因子ICIR评测"""
    serializer_class = FvICIRReviewSerializer

    def create(self, request, *args, **kwargs):
        file = File(request.FILES['file'])
        factor = FvSeqReviewICIR(file.df)
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            factor.earn = FvFactoryEarnings().make_earnings(factor.stime, factor.etime, serializer.data['earnings_fun'])
            factor.windows = serializer.data['windows']  # 收益方法
            factor.periods = serializer.data['periods_list']
            factor.correlation = serializer.data['correlation']
            data = factor.cal_main()
        except Exception as e:
            raise CommonException(400, str(e))

        return Response({file.name: data})


class FvRedisIcIr(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
      时序期货
      get ICIR by redis
      """
    serializer_class = FvIcIrRedisSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        table_type = serializer.data['table_type']
        corr_label = serializer.data['corr_label']
        windows = serializer.data['windows']
        corr = serializer.data['corr']
        windows = int(windows) if windows != "till_now" else windows

        summary = cache.get(table_type)[windows][corr_label]
        charts = cache.get(f'charts_{table_type}')

        ic = self._resp_charts_data(charts, corr, corr_label)
        ic['trading_date'] = list(charts[windows][corr][corr_label].index.astype(str))
        cum_sum_ic = self._resp_ml_cum_ic(charts[windows][corr][corr_label])

        result = {
            'table': summary,
            'charts': {'ic': ic, 'cum_ic': cum_sum_ic},

        }
        return Response(result, status=status.HTTP_201_CREATED)

    def _resp_charts_data(self, data, corr, corr_label):
        result = {}
        for w, windows in data.items():
            label = windows[corr][corr_label]
            label.sort_index(inplace=True)
            # label.dropna(inplace=True)
            for key, val in label.items():
                val = np.where(val.notnull(), val, None)
                data = {
                    'name': f'corr_{w}',
                    'type': 'line',
                    'data': val,
                    'showSymbol': False,
                }
                if not result.get(key):
                    result[key] = []
                result[key].append(data)
        return result

    def _resp_ml_cum_ic(self, data):
        data.sort_index(inplace=True)
        data = data.cumsum().fillna('')
        data.reset_index(inplace=True)
        data['trading_date'] = data['trading_date'].astype(str)
        result = {val: data[val].tolist() for val in data}
        return result


class FvCalCorr(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    期货时序相关性
    """
    serializer_class = FvCorrSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        factor = FvSeqAnalysisCorr()
        factor.sort = serializer.data['factor_sort']
        factor.stime = serializer.data['stime']
        factor.etime = serializer.data['etime']
        t_service = TableTypeFactory.make_table(serializer.data['table_name'], factor)
        result = t_service.cal_merge_factor(serializer.data['factor'])

        return Response(result)
