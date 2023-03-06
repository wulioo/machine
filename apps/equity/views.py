import json

import pandas as pd
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from apps.equity.serializers import FactorEquityIcIrSerializer, FactorEqZonalTestingSerializer, FactorEqNdcgSerializer, FactorEqReviewSerializer, FactorEqDistributeSerializer, \
    FactorEqLayeredReviewSerializer, FactorEqCorrSerializer, FactorEqBacktestingSerializer, FactorEqVarieAvgSerializer
from apps.future.serializers import FactorNDCGReviewSerializer, FactorCorrSerializer, FactorBacktestingSerializer, FactorDistributeSerializer, FactorBacktestingReviewSerializer
from service.earnings import  EquityEarnings
from service.section.avg_varie import EqFactorAvgVarie
from service.section.backtesting import EqFactorBackTesting
from service.section.distribute import EqFactorDistribute
from service.section.icir import EqFactorICIR
from service.section.layered import EqLayeredFactor
from service.section.ndcg import EqFactorNdcg
from service.file import File
from service.layered import LayeredTest, LayeredBackTestIng
from service.table_name import Table
from utils.common import Common
from utils.exception import CommonException


class FactorCalEquityIcIr(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    计算股票ICIR1
    """
    serializer_class = FactorEquityIcIrSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        stime = serializer.data['stime']
        etime = serializer.data['etime']
        earnings_fun = serializer.data['earnings_fun']  # 收益方法
        cal_ear = EarningsFactory.create_earnings(earnings_fun)
        factor_diff = serializer.data['factor_diff']  # 因子差异
        redis_key = serializer.data['redis_key']  # 指数选择
        result = []
        factor = EqFactorICIR()
        factor.periods = serializer.data['periods']  # 收益周期
        factor.correlation = serializer.data['correlation']  # 相关系数
        factor.sort = serializer.data['factor_sort']  # 因子排名
        factor.index_code = serializer.data['index_code']  # 指数选择

        factor.earn = EquityEarnings(stime, etime, cal_ear)
        factor.stime = stime
        factor.etime = etime
        for table, future in serializer.data['factor'].items():
            factor.model = Common.get_models('db', table)
            factor.column = future.get('factor_list')  # 因子
            factor_df = factor.get_eq_factor()
            ic_data, summary_data = factor.cal_table_icir(factor_df, factor_diff)

            res = {'ic': ic_data, 'summary': summary_data, 'table': table}
            result.append(res)

        tmp_res = {}
        for res in result:
            data = factor.save_redis(res['table'], res['ic'], res['summary'], redis_key)
            tmp_res.update(data)

        return Response(tmp_res, status=status.HTTP_201_CREATED)


class FactorEqZonalTesting(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    股票分层测试
    """
    serializer_class = FactorEqZonalTestingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stime = serializer.data['stime']
        etime = serializer.data['etime']
        redis_key = serializer.data['redis_key']
        earnings_fun = serializer.data['earnings_fun']  # 收益方法
        cal_ear = EarningsFactory.create_earnings(earnings_fun)

        layered = LayeredTest()
        earn = EquityEarnings(stime, etime, cal_ear)
        factor = EqLayeredFactor(layered, earn)
        factor.stime = stime
        factor.etime = etime
        factor.layered.num = serializer.data['layered_num']
        factor.periods = serializer.data['periods']
        factor.index_code = serializer.data['index_code']  # 指数选择
        # layered_service = FactorLayeredService(layered, earn)
        data = {}
        for table, future in serializer.data['factor'].items():
            factor.model = Common.get_models('db', table)
            factor.column = future.get('factor_list')  # 因子列表
            layered_fun = future.get('layered_fun')  # 分层方法
            # 1.从因子库找到对应的因子字段 以及 wind_code 或者type_name_ab
            factor_arr = factor.get_eq_factor()

            # 5.计算收益率
            data[table] = factor.layered_test(factor_arr, table, redis_key)

        return Response(data, status=status.HTTP_201_CREATED)


class FactorEqNdcg(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    股票 NDCG 计算
    """
    serializer_class = FactorEqNdcgSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stime = serializer.data['stime']
        etime = serializer.data['etime']
        earnings_fun = serializer.data['earnings_fun']  # 收益方法
        cal_ear = EarningsFactory.create_earnings(earnings_fun)
        earn = EquityEarnings(stime, etime, cal_ear)
        factor = EqFactorNdcg()
        factor.earn = earn
        factor.stime = stime
        factor.etime = etime
        factor.index_code = serializer.data['index_code']  # 指数选择
        factor.periods = serializer.data['periods']
        # 5.计算收益率

        rsp_result = {}
        for table, future in serializer.data['factor'].items():
            factor.model = Common.get_models('db', table)
            factor.column = future.get('factor_list')  # 因子

            factor_arr = factor.get_eq_factor()
            # 计算ndcg
            rsp_result[table] = factor.cal_ndcg(factor_arr)

        return Response(rsp_result)


class FactorEqCorr(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    股票 相关性
    """
    serializer_class = FactorEqCorrSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        factor = EqFactorCorr()
        factor.sort = serializer.data['factor_sort']
        factor.stime = serializer.data['stime']
        factor.etime = serializer.data['etime']
        t_service = Table()

        result = t_service.cal_merge_factor(factor, serializer.data['factor'])

        return Response(result.fillna(0))


class FactorEqBacktesting(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorEqBacktestingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        stime = serializer.data['stime']
        etime = serializer.data['etime']
        layered = LayeredBackTestIng()
        earnings_fun = serializer.data['earnings_fun']  # 收益方法
        cal_ear = EarningsFactory.create_earnings(earnings_fun)
        earn = EquityEarnings(stime, etime, cal_ear)
        factor = EqFactorBackTesting(layered, earn)
        factor.stime = stime
        factor.etime = etime
        factor.index_code = serializer.data['index_code']  # 指数选择
        factor.layered.num = serializer.data['layering']
        factor.periods = serializer.data['periods']
        factor_item = serializer.data['factor']
        result = dict()
        for table, future in factor_item.items():
            factor.model = Common.get_models('db', table)
            factor.column = future.get('factor_list')  # 因子列表
            # 1.从因子库找到对应的因子字段 以及 wind_code 或者type_name_ab
            factor_df = factor.get_eq_factor()
            result[table] = factor.layered_backtesting(factor_df)

        return Response(result, status=status.HTTP_201_CREATED)


class FactorEqDistribute(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorEqDistributeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        factor = EqFactorDistribute()
        factor.stime = serializer.data['stime']
        factor.etime = serializer.data['etime']
        factor.sort = serializer.data['factor_sort']
        factor.index_code = serializer.data['index_code']  # 指数选择
        result = {}
        for table, future in serializer.data['factor'].items():
            factor.model = Common.get_models('db', table)
            factor.column = future.get('factor_list')  # 因子
            factor_df = factor.get_eq_factor()

            factor_df = factor.box_chart_factor_sort(factor_df) if factor.sort else factor_df
            result[table] = factor.celery_box_muster_chart(factor_df)
            # result[table] = future.single_box_muster_chart(factor_df)
        return Response(result, status=status.HTTP_201_CREATED)


class FactorEqICIRReview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """股票因子ICIR评测"""
    serializer_class = FactorEqReviewSerializer

    def create(self, request, *args, **kwargs):
        file = File(request.FILES['file'])
        df = file.df
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            stime = str(df['trading_date'].min())

            etime = str(df['trading_date'].max())

            #  ================ 测代码 ================
            # df = df[df['trading_date'].astype(str) > '2022-07-01']
            # stime = '2022-09-01'
            # etime = '2022-11-17'
            #  ================ 测代码 ================
            redis_key = serializer.data['redis_key']  # 因子排名
            earnings_fun = serializer.data['earnings_fun']  # 收益方法
            cal_ear = EarningsFactory.create_earnings(earnings_fun)
            factor = EqFactorICIR()
            factor.periods = serializer.data['periods']  # 收益周期
            factor.correlation = serializer.data['correlation']  # 相关系数
            factor.sort = serializer.data['factor_sort']  # 因子排名
            factor.earn = EquityEarnings(stime, etime, cal_ear)

            factor_diff = serializer.data['factor_diff']  # 因子差异
            factor.column = df.drop(labels=['trading_date', 'wind_code'], axis=1).columns.tolist()

            df.dropna(subset=['wind_code'], inplace=True)
            ic_data, summary_data = factor.cal_table_icir(df, factor_diff)

            result = factor.save_redis('tem_eq_icir', ic_data, summary_data, redis_key)
        except Exception as e:
            raise CommonException(400, str(e))

        return Response(result)


class FactorEqCorrReview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorCorrSerializer

    def create(self, request, *args, **kwargs):
        file = File(request.FILES['file'])
        file_df = file.df
        stime = str(file.df['trading_date'].min())
        etime = str(file.df['trading_date'].max())
        file_cols = list(file.df.drop(labels=['trading_date', 'wind_code'], axis=1).columns.values)

        factor = EqFactorCorr()
        factor.stime = stime
        factor.etime = etime
        factor.sort = request.data['factor_sort']
        factor_item = json.loads(request.data['factor'])
        try:
            tables = []
            for table, future in factor_item.items():
                factor.model = Common.get_models('db', table)
                factor.column = future.get('factor_list')  # 因子
                factor_arr = factor.get_factor_value()
                factor_arr = factor.get_factor_sort(factor_arr) if factor.sort == 'true' else factor_arr

                tables.append(factor_arr)
            factor_list = tables[0]
            if len(tables) > 1:
                for i in (range(len(tables) - 1)):
                    factor_list2 = tables[i + 1]
                    factor_list = factor_list.merge(factor_list2, how="outer", on=['trading_date', 'wind_code'])
            # 文件因子排序
            factor.column = file_cols
            file_df = factor.get_factor_sort(file_df) if factor.sort == 'true' else file_df

            factor_list = file_df.merge(factor_list, how="outer", on=['trading_date', 'wind_code'])
            df = factor_list.drop(labels=['trading_date', 'wind_code'], axis=1)
        except Exception as e:
            df = file_df.drop(labels=['trading_date', 'wind_code'], axis=1)

        result = df.corr()
        result = result[factor.column] if factor.sort == 'true' else result[file_cols]

        return Response({'data': result, 'index_col': result.index})


class FactorEqDistributeReview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorDistributeSerializer

    def create(self, request, *args, **kwargs):
        file = File(request.FILES['file'])
        file_df = file.df
        stime = str(file_df['trading_date'].min())
        etime = str(file_df['trading_date'].max())
        factor = EqFactorDistribute()
        result = factor.celery_box_muster_chart(file_df)
        return Response({file.name: result}, status=status.HTTP_201_CREATED)


class FactorEqBackTestIngReview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorBacktestingReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = File(request.FILES['file'])
        stime = str(file.df['trading_date'].min())
        etime = str(file.df['trading_date'].max())
        earnings_fun = serializer.data['earnings_fun']  # 收益方法
        cal_ear = EarningsFactory.create_earnings(earnings_fun)
        earn = EquityEarnings(stime, etime, cal_ear)
        layered = LayeredBackTestIng()
        factor = EqFactorBackTesting(layered, earn)
        factor.stime = stime
        factor.etime = etime
        factor.periods = serializer.data['periods']
        factor.layered.num = serializer.data['layering']
        type_name = file.df.columns.tolist()[1]
        factor.column = list(file.df.drop(labels=[file.df.columns.tolist()[0], type_name], axis=1).columns.values)

        result = factor.layered_backtesting(file.df)
        return Response({file.name: result})
class FactorEqAvgVarie(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorEqVarieAvgSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        factor = EqFactorAvgVarie()
        factor.stime = serializer.data['stime']
        factor.etime = serializer.data['etime']
        factor.index_code = serializer.data['index_code']  # 交易所
        table_df = pd.DataFrame(columns=['trading_date', 'wind_code'])
        for table, future in serializer.data['factor'].items():
            factor.model = Common.get_models('db', table)
            factor.column = future.get('factor_list')  # 因子
            factor_df = factor.get_eq_factor()
            table_df = table_df.merge(factor_df, how='outer', on=['trading_date', 'wind_code'])
        coverage = factor.cal_coverage(table_df)
        # 渲染
        return Response(list(json.loads(coverage.T.to_json()).values()), status=status.HTTP_201_CREATED)


class FactorEqZonalTestingReview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FactorEqLayeredReviewSerializer

    def create(self, request, *args, **kwargs):
        file = File(request.FILES['file'])
        df = file.df
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        redis_key = serializer.data['redis_key']
        stime = str(df['trading_date'].min())
        etime = str(df['trading_date'].max())
        factor_neu = serializer.data['factor_neu']  # 分层方法

        # ================ 测代码 ================
        # df = df[df['trading_date'].astype(str) > '2022-07-01']
        # stime = '2022-07-01'
        # etime = '2022-08-17'
        # ================ 测代码 ================
        earnings_fun = serializer.data['earnings_fun']  # 收益方法
        cal_ear = EarningsFactory.create_earnings(earnings_fun)
        layered = LayeredTest()
        earn = EquityEarnings(stime, etime, cal_ear)
        factor = EqLayeredFactor(layered, earn)
        factor.stime = stime
        factor.etime = etime
        factor.layered.num = serializer.data['layered_num']
        factor.periods = serializer.data['periods']
        # 5.计算收益率

        factor.column = df.drop(labels=['trading_date', 'wind_code'], axis=1).columns.tolist()
        df.dropna(subset=['wind_code'], inplace=True)

        result = factor.layered_test(df, file.name, redis_key)

        return Response({file.name: result}, status=status.HTTP_201_CREATED)


class FactorEqNDCGReview(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """因子NDCG评测"""
    serializer_class = FactorNDCGReviewSerializer

    def create(self, request, *args, **kwargs):
        file = File(request.FILES['file'])
        df = file.df

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            stime = str(df['trading_date'].min())
            etime = str(df['trading_date'].max())

            # ================ 测代码 ================
            # df = df[df['trading_date'].astype(str) > '2022-07-01']
            # stime = '2022-07-01'
            # etime = '2022-08-17'
            # ================ 测代码 ================
            earnings_fun = serializer.data['earnings_fun']  # 收益方法
            cal_ear = EarningsFactory.create_earnings(earnings_fun)
            earn = EquityEarnings(stime, etime, cal_ear)
            factor = EqFactorNdcg()
            factor.earn = earn
            factor.stime = stime
            factor.etime = etime
            factor.periods = serializer.data['periods']
            factor.column = df.drop(labels=['trading_date', 'wind_code'], axis=1).columns.tolist()
            df.dropna(subset=['wind_code'], inplace=True)
            # 计算ndcg
            result = factor.cal_ndcg(df)
        except Exception as e:
            raise CommonException(400, str(e))

        return Response({file.name: result})
