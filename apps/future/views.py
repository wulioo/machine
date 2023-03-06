import json
import os
import re
import uuid

import numpy as np
from django.core.cache import cache
from matplotlib import pyplot as plt

from Machine.settings import STATICFILES_DIRS, BASE_DIR
from extra.db.models_tqfactor import FactorCategoryInfo, FvFactorInfo
from extra.db.models_tqmain import FutureHeader, FutureDominantDaily, FutureDaily
from extra.db.models_tqsignal import SignalCategoryInfo, FvSignalInfo
from extra.factory.earnings import FvFactoryEarnings
from extra.factory.positioning import PositioningFactory, FvPositioning
from extra.factory.table_name import TableTypeFactory
from logs import logger

from django.core.exceptions import FieldError
from django.db.models import Q, Count, Sum
import pandas as pd
from rest_framework import mixins, viewsets, status
from rest_framework.views import APIView
import warnings
from rest_framework.response import Response

from service.db import MysqlDb
from service.section.avg_varie import FvFactorAvgVarie, FvSecAnalyAvgVarie
from service.section.backtesting import FvSecAnalyBackTesting, FvSecReviewBackTesting
from service.section.corr import FvSecAnalysisCorr, FvSecReviewCorr
from service.section.earnings import FvSecAnalyEarnings
from service.section.icir import FvSecAnalysisICIR, EqFactorICIR, FvSecOneReviewICIR, FvSecTwoReviewICIR

from service.section.distribute import FvSecAnalyDistribute, FvSecReviewDistribute
from service.section.layered import FactorLayered, FvSecAnalyLayered, FvSecOneReviewLayered, FvSecTwoReviewLayered
from service.section.ndcg import FvSecAnalyNdcg, FvSecReviewNdcg
from service.periods import SinglePeriods, ManyPeriods
from service.varieties import Varieties, VarietiesFactory
from utils.config import EXCHANGE_FUTURE, TABLENAME
from apps.future.models import SysTable, FutureDailyType
from apps.future.serializers import FactorIcIrSerializer, FactorZonalTestingSerializer, FactorCacheICSerializer, \
    FactorCacheEchartsSerializer, FactorNdcgSerializer, FactorReviewSerializer, \
    FactorNDCGReviewSerializer, FactorLayeredReviewSerializer, FactorCorrSerializer, \
    FactorFvEarnings, FactorFvSharpeEarnings, \
    FactorVarieAvgSerializer, FactorDistributeSerializer, FactorTableMinxin, FactorPositioningSerializer, \
    FactorBacktestingSerializer, RedisKeyMinxin, FactorBacktestingReviewSerializer
from service.earnings import FutureEarnings, CloseEarnings, EquityEarnings

from service.file import File
from service.layered import Layered, LayeredTest, LayeredBackTestIng
from utils.code import StatusCode, PlatformCode, TableTypeCode, FileNumber

from utils.common import Common, TimeContext
from utils.exception import CommonException, ResultEmpty

warnings.filterwarnings('ignore')


class FactorList(APIView):
    _db: str
    _info_model: None

    def get(self, request, *args, **kwargs):
        self._db = TABLENAME.get(request.query_params['type'])
        platform = request.query_params['platform']
        if request.query_params['type'] == 'fac_table':
            self._info_model = FvFactorInfo
        else:
            self._info_model = FvSignalInfo
        result = []
        if int(platform) == 2:
            sys_table = SysTable.get_info_all(Q(tb_type=platform) & Q(status=1), ['tb_name'])
            for table in sys_table['tb_name']:
                ret = dict()
                ret['value'] = table  # 表名
                ret['label'] = table
                ret['children'] = []  # type_name_ab

                field_live = self.setEqField('live', table)
                ret['children'].append(field_live)
                result.append(ret)
        else:
            sys_table = self._info_model.get_duplication_field('table_name', self._db)
            for table in sys_table['table_name']:
                ret = dict()
                ret['value'] = table
                ret['label'] = table
                ret['children'] = []

                for val in ['live', 'dead']:
                    field_live = self.setFvField(val, Q(table_name=table) & Q(status=val))
                    ret['children'].append(field_live)
                result.append(ret)
        return Response(sorted(result, key=lambda x: x['value'], reverse=False))

    def setFvField(self, factor_label, conditions):
        factor_df = self._info_model.get_info_all(conditions, ['factor_name', 'status'], self._db)

        field = {
            'value': factor_label,
            'label': factor_label,
            'children': []
        }
        if factor_df.empty:
            return field
        factor_df.sort_values(by='factor_name', inplace=True, ascending=True)
        for key, val in factor_df.iterrows():
            tmp_dict = {
                'value': val.loc['factor_name'],
                'label': val.loc['factor_name'],
            }
            field['children'].append(tmp_dict)
        return field

    def setEqField(self, factor_label, table):
        model = Common.get_models('db', table)
        field_list = [field.name for field in model._meta.get_fields()]
        rv_field = ['trading_date', 'upload_user', 'upload_time', 'last_tradedate', 'wind_code']
        tmp_field = [f for f in field_list if f not in rv_field]
        field = {
            'value': factor_label,
            'label': factor_label,
            'children': []
        }
        for f_name in tmp_field:
            tmp_dict = {
                'value': f_name,
                'label': f_name,
            }
            field['children'].append(tmp_dict)
        return field


class FactorCategoryList(APIView):
    _db: str
    _cgy_model: None
    _info_model: None

    def get(self, request, *args, **kwargs):
        self._db = TABLENAME.get(request.query_params['type'])
        platform = request.query_params['platform']
        if request.query_params['type'] == 'fac_category':
            self._cgy_model = FactorCategoryInfo
            self._info_model = FvFactorInfo
        else:
            self._cgy_model = SignalCategoryInfo
            self._info_model = FvSignalInfo
        # self._cgy_model = cgy_model
        category = self._cgy_model.get_info_all(Q(pid=0) & Q(instrument_type='future'), [], self._db)
        result = []
        for key, cg_one in category.iterrows():
            ret = dict()
            ret['value'] = cg_one.category_name  # 表名
            ret['label'] = cg_one.category_name
            ret['children'] = []  # type_name_ab
            category_one = self._cgy_model.get_info_all(Q(pid=cg_one.category_id) & Q(instrument_type='future'), [], self._db)
            # if type == 'fac_category':
            #     category_one = FactorCategoryInfo.get_info_all(Q(pid=cg_one.category_id) & Q(instrument_type='future'), [], self._db)
            # else:
            #     category_one = SignalCategoryInfo.get_info_all(Q(pid=cg_one.category_id) & Q(instrument_type='future'), [], self._db)

            for index, cg_two in category_one.iterrows():
                category_two = {
                    'value': cg_two.category_name,
                    'label': cg_two.category_name,
                    'children': []
                }
                for val in ['live', 'dead']:
                    table_status = self.setField(Q(category2=cg_two.category_name) & Q(status=val))
                    temp_dict = {
                        'value': val,
                        'label': val,
                        'children': table_status
                    }
                    category_two['children'].append(temp_dict)

                ret['children'].append(category_two)
            result.append(ret)
        return Response(sorted(result, key=lambda x: x['value'], reverse=False))

    def setField(self, conditions):
        category_three = self._info_model.get_info_all(conditions, ['factor_name', 'table_name'], self._db)
        table_info = []
        if category_three.empty:
            return table_info
        # 找到重复值
        dup_factor = self._info_model.get_distinct_field('factor_name', self._db)
        for key, val in category_three.iterrows():
            if val['factor_name'] in dup_factor:
                factor_name = val['table_name'] + '.' + val['factor_name']
            else:
                factor_name = val['factor_name']
            table_info.append({
                'value': factor_name,
                'label': factor_name
            })
        return table_info


class FvCalICIR(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    期货计算ICIR
    """
    serializer_class = FactorIcIrSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        stime = serializer.data['stime']
        etime = serializer.data['etime']

        vits_fun = serializer.data['varieties']  # 标的方法

        factor = FvSecAnalysisICIR()
        factor.earn = FvFactoryEarnings().make_earnings(stime, etime, serializer.data['earnings_fun'])
        factor.vari = VarietiesFactory.create_varieties(vits_fun)
        factor.sort = serializer.data['factor_sort']  # 因子排名
        factor.night = serializer.data['night_trading']
        factor.diff = serializer.data['factor_diff']  # 因子差异
        factor.stime = stime
        factor.etime = etime
        factor.exchange = serializer.data['exchange_future']  # 交易所
        factor.periods = serializer.data['periods']  # 收益周期
        factor.correlation = serializer.data['correlation']  # 相关系数
        factor_service = TableTypeFactory.make_table(serializer.data['table_name'], factor)
        result = factor_service.main(serializer.data['factor'])
        return Response(result, status=status.HTTP_201_CREATED)


class FactorZonalTesting(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    期货分层测试
    """
    serializer_class = FactorZonalTestingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stime = serializer.data['stime']
        etime = serializer.data['etime']
        layered_fun = serializer.data['layered_fun']  # 分层方法
        redis_key = serializer.data['redis_key']  # 分层层数
        layered = LayeredTest()
        layered.num = serializer.data['layered_num']
        earn = FvFactoryEarnings().make_earnings(stime, etime, serializer.data['earnings_fun'])
        factor = FvSecAnalyLayered()
        factor.set_layered(layered)
        factor.set_earn(earn)
        factor.set_vari(serializer.data['varieties'])
        factor.stime = stime
        factor.etime = etime
        factor.night = serializer.data['night_trading']
        factor.exchange = serializer.data['exchange_future']  # 交易所
        factor.periods = serializer.data['periods']  # 收益周期
        factor_service = TableTypeFactory.make_table(serializer.data['table_name'], factor)
        result = factor_service.cal_layered(serializer.data['factor'], redis_key)

        return Response(result, status=status.HTTP_201_CREATED)


class FactorFvNdcg(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    期货 NDCG 计算
    """
    serializer_class = FactorNdcgSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stime = serializer.data['stime']
        etime = serializer.data['etime']
        factor = FvSecAnalyNdcg()
        factor.earn = FvFactoryEarnings().make_earnings(stime, etime, serializer.data['earnings_fun'])
        factor.vari = VarietiesFactory.create_varieties(serializer.data['varieties'])  # 标的方法
        factor.stime = stime
        factor.etime = etime
        factor.night = serializer.data['night_trading']
        factor.exchange = serializer.data['exchange_future']  # 交易所
        factor.periods = serializer.data['periods']  # 收益周期
        factor_service = TableTypeFactory.make_table(serializer.data['table_name'], factor)

        result = factor_service.main(serializer.data['factor'])

        return Response(result)


class FutureFactorCorr(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    期货股票 相关性
    """
    serializer_class = FactorCorrSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        factor = FvSecAnalysisCorr()
        factor.sort = serializer.data['factor_sort']
        factor.stime = serializer.data['stime']
        factor.etime = serializer.data['etime']
        factor.night = serializer.data['night_trading']
        factor_service = TableTypeFactory.make_table(serializer.data['table_name'], factor)
        result = factor_service.cal_merge_factor(serializer.data['factor'])

        return Response(result)


class FactorICIRReview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """期货因子ICIR评测"""
    serializer_class = FactorReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if len(request.FILES) == FileNumber.ONEFILE.value:
            file = File(request.FILES['factor'])
            factor = FvSecOneReviewICIR(file.df)
            factor.earn = FvFactoryEarnings().make_earnings(factor.stime, factor.etime, serializer.data['earnings_fun'])
        else:
            file_one = File(request.FILES['factor'])
            file_two = File(request.FILES['label'])
            factor = FvSecTwoReviewICIR(file_one.df, file_two.df)
            factor.earn = FvFactoryEarnings().make_earnings(factor.stime, factor.etime, 'file_price')

        factor.diff = serializer.data['factor_diff']  # 因子差异
        factor.correlation = serializer.data['correlation']
        factor.sort = serializer.data['factor_sort']  # 因子排名
        factor.periods = serializer.data['periods']
        result = factor.cal_main()
        return Response({"factor_ic_temp": result})


class FactorZonalTestingReview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    期货分层评测
    """
    serializer_class = FactorLayeredReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if len(request.FILES) == FileNumber.ONEFILE.value:
            file = File(request.FILES['factor'])
            factor = FvSecOneReviewLayered(file.df)
            earn = FvFactoryEarnings().make_earnings(factor.stime, factor.etime, serializer.data['earnings_fun'])

        else:
            file_one = File(request.FILES['factor'])
            file_two = File(request.FILES['label'])
            factor = FvSecTwoReviewLayered(file_one.df, file_two.df)
            earn = FvFactoryEarnings().make_earnings(factor.stime, factor.etime, 'file_price')
        layered = LayeredTest()
        layered.num = serializer.data['layered_num']
        factor.set_earn(earn)
        factor.set_layered(layered)
        factor.periods = serializer.data['periods']
        redis_key = serializer.data['redis_key']
        result = factor.resp_layered(factor.cal_main(), "factor_layered_temp", redis_key)
        return Response({"factor_layered_temp": result}, status=status.HTTP_201_CREATED)


class FactorNDCGReview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """因子NDCG评测"""
    serializer_class = FactorNDCGReviewSerializer

    def create(self, request, *args, **kwargs):
        file = File(request.FILES['file'])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            factor = FvSecReviewNdcg(file.df)
            factor.earn = FvFactoryEarnings().make_earnings(factor.stime, factor.etime, serializer.data['earnings_fun'])
            factor.periods = serializer.data['periods']

            # 计算ndcg
            result = factor.cal_main()
        except Exception as e:
            raise CommonException(400, str(e))

        return Response({file.name: result})


class FactorCorrReview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorCorrSerializer

    def create(self, request, *args, **kwargs):
        file = File(request.FILES['file'])
        factor = FvSecReviewCorr(file.df)
        factor.sort = request.data['factor_sort']
        factor_item = json.loads(request.data['factor'])
        factor_service = TableTypeFactory.make_table(request.data['table_name'], factor)
        result = factor_service.cal_merge_factor(factor_item)

        return Response({'data': result, 'index_col': result.index})


class FactorIcByRedis(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """redis缓存取数据"""
    serializer_class = FactorCacheICSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        res = cache.get(data["redis_key"])
        if res is None:
            raise ResultEmpty()
        df = res[data["correlation"]][data["corr_label"]].fillna(0).round(4)
        df.reset_index(inplace=True)

        if data["correlation"] == 'summary':
            df_col = [df_col for df_col in list(df.columns) if '>' in df_col or '<' in df_col]
            for col in df_col:
                df[col] = round(df[col] * 100, 2).astype(str) + '%'

        data = [dict(df.iloc[index]) for index in df.index]
        return Response(data, status=status.HTTP_201_CREATED)


class FactorCorrByRedis(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorCacheICSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        data = cache.get(data['redis_key'])[data['correlation']][data['corr_label']]
        ic = self._resp_ml_ic(data)
        cum_sum_ic = self._resp_ml_cum_ic(data)
        return Response({'ic': ic, 'cum_ic': cum_sum_ic}, status=status.HTTP_201_CREATED)

    def _resp_ml_ic(self, data):
        """
        数据格式转换
        :param data:
        :return:
        """
        data.sort_index(inplace=True)
        temp_arr = {}
        for key, val in data.items():
            mean = [{
                'name': key,
                'type': 'line',
                'data': val.fillna(''),
                'showSymbol': False,
            }]
            for num_mean in [60, 120, 240, 480]:
                # 去缺省值
                temp_data = val.rolling(num_mean).mean()
                temp_data = np.where(temp_data.notnull(), temp_data, '')
                temp_dict = {
                    'name': key + '_MA' + str(num_mean),
                    'type': 'line',
                    'data': temp_data,
                    'showSymbol': False,
                }
                mean.append(temp_dict)
            temp_arr[key] = mean
        temp_arr['data'] = data.index
        return temp_arr

    def _resp_ml_cum_ic(self, data):
        data.sort_index(inplace=True)
        data = data.cumsum().fillna('')
        data.reset_index(inplace=True)
        result = {val: data[val].tolist() for val in data}
        return result


class FactorEchartsByRedis(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """redis缓存取Echarts数据"""
    serializer_class = FactorCacheEchartsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        key = f'{data["table_name"]}-{data["factor"]}-{data["group_name"]}-{data["factor_label"]}-{data["redis_key"]}'
        res = cache.get(key)
        if res is None:
            raise ResultEmpty()
        for val in res:
            # ??这里的NAN 是变0还是删除？ 疑问
            if isinstance(val, dict):
                val['data'] = pd.Series(data=val['data']).fillna(0)

        return Response({'data': res}, status=status.HTTP_201_CREATED)


class FactorCalEarnings(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorFvEarnings

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stime = serializer.data['stime']
        etime = serializer.data['etime']
        earn = FvFactoryEarnings().make_earnings(stime, etime, serializer.data['earnings_fun'])
        factor = FvSecAnalyEarnings(earn, serializer.data['periods'])
        factor.stime = stime
        factor.etime = etime
        factor.exchange = serializer.data['exchange_future']  # 交易所
        result = factor.cal_main()
        return Response(result, status=status.HTTP_201_CREATED)


class FactorCalSharpeEarnings(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorFvSharpeEarnings

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stime = serializer.data['stime']
        etime = serializer.data['etime']
        earn = FvFactoryEarnings().make_earnings(stime, etime, serializer.data['earnings_fun'])
        earn.cal_ear.sharpe = True

        factor = FvSecAnalyEarnings(earn, serializer.data['periods'])
        factor.stime = stime
        factor.etime = etime
        factor.exchange = serializer.data['exchange_future']  # 交易所
        result = factor.cal_main()
        return Response(result, status=status.HTTP_201_CREATED)


class FactorFvAvgVarie(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorVarieAvgSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        factor = FvSecAnalyAvgVarie()
        factor.stime = serializer.data['stime']
        factor.etime = serializer.data['etime']
        factor.exchange = serializer.data['exchange_future']  # 交易所
        factor.night = serializer.data['night_trading']
        factor_service = TableTypeFactory.make_table(serializer.data['table_name'], factor)
        coverage = factor_service.cal_merge_factor(serializer.data['factor'])
        return Response(list(json.loads(coverage.T.to_json()).values()), status=status.HTTP_201_CREATED)


#

class FutureFactorDistribute(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorDistributeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        factor_item = serializer.data['factor']
        factor = FvSecAnalyDistribute()
        factor.stime = serializer.data['stime']
        factor.etime = serializer.data['etime']
        factor.night = serializer.data['night_trading']
        factor.sort = serializer.data['factor_sort']
        factor.exchange = serializer.data['exchange_future']
        factor_service = TableTypeFactory.make_table(serializer.data['table_name'], factor)
        result = factor_service.main(factor_item)

        return Response(result, status=status.HTTP_201_CREATED)


class FvFactorReviewDistribute(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorDistributeSerializer

    def create(self, request, *args, **kwargs):
        file = File(request.FILES['file'])
        factor = FvSecReviewDistribute(file.df)
        result = factor.cal_main()
        return Response({file.name: result}, status=status.HTTP_201_CREATED)


class FactorFvPositioning(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorPositioningSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        weight = serializer.data['weight']
        money = serializer.data['money']
        type_name_ab = serializer.data['type_name_ab']
        factor = PositioningFactory.make_positioning(FvPositioning(), serializer.data['periods'])

        # section.stime = serializer.data['cur_time']
        factor.stime = Common.get_previous_trading_time(serializer.data['cur_time'])
        factor.layered.num = serializer.data['layering']
        factor.periods.label = serializer.data['periods']
        factor.night = serializer.data['night_trading']
        factor_item = serializer.data['factor']
        factor_service = TableTypeFactory.make_table(serializer.data['table_name'], factor)

        result = factor_service.cal_positing(factor_item, weight, money, type_name_ab)

        return Response(result, status=status.HTTP_201_CREATED)


class FactorFvBacktesting(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorBacktestingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        layered = LayeredBackTestIng()
        layered.num = serializer.data['layering']
        factor = FvSecAnalyBackTesting()
        factor.stime = serializer.data['stime']
        factor.etime = serializer.data['etime']
        factor.set_earn(serializer.data['earnings_fun'])
        factor.set_layered(layered)

        factor.night = serializer.data['night_trading']
        factor.exchange = serializer.data['exchange_future']
        factor.periods = serializer.data['periods']
        factor_item = serializer.data['factor']
        factor_service = TableTypeFactory.make_table(serializer.data['table_name'], factor)

        result = factor_service.main(factor_item)

        return Response(result, status=status.HTTP_201_CREATED)


class FvFactorBackTestIngReview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorBacktestingReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = File(request.FILES['file'])
        factor = FvSecReviewBackTesting(file.df)
        layered = LayeredBackTestIng()
        layered.num = serializer.data['layering']
        factor.set_earn(serializer.data['earnings_fun'])
        factor.set_layered(layered)
        factor.periods = serializer.data['periods']

        result = factor.cal_main()
        return Response({file.name: result})


class FvFactorBacktestingByRedis(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RedisKeyMinxin

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        redis_key = serializer.data['redis_key']
        result = cache.get(redis_key)
        return Response(result, status=status.HTTP_201_CREATED)


class GetMysqlData(APIView):
    def get(self, request, *args, **kwargs):
        num = int(request.query_params['num'])

        sql = f"""SELECT * FROM `equity_daily`
                            WHERE trading_date between '2022-0{num}-01' AND '2022-0{num + 1}-01';"""
        with MysqlDb() as db:
            data = pd.read_sql(sql, con=db.conn).to_json()

        return Response(data, status=status.HTTP_201_CREATED)
