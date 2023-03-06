import json

from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.future.models import SysTable
from apps.future.serializers import FactorIcIrSerializer
from extra.db.models_tqfactor import FvFactorInfo, FactorCategoryInfo
from extra.factory.earnings import FvFactoryEarnings
from service.section.icir import FvSecAnalysisICIR
from service.table_type import FactorSingleTable
# from service.table_type import SingleTable
from service.varieties import VarietiesFactory
from utils.common import Common
from utils.exception import CommonException


class FactorApiList(APIView):
    def get(self, request, *args, **kwargs):
        type = request.query_params['type']
        # 获取所有表名
        result = dict()
        if type == "table":
            sys_table = FvFactorInfo.get_duplication_field('table_name', 'tq_factor')
            sys_table.sort_values(by='table_name', inplace=True)
            for table in sys_table['table_name']:
                result[table] = dict()  # 表名
                for val in ['live', 'dead']:
                    result[table][val] = self.setFvTbleField(Q(table_name=table) & Q(status=val))
        elif type == "category":
            category = FactorCategoryInfo.get_info_all(Q(pid=0) & Q(instrument_type='future'), [], 'tq_factor')
            for key, cg_one in category.iterrows():
                result[cg_one.category_name] = dict()  # 表名
                category_one = FactorCategoryInfo.get_info_all(Q(pid=cg_one.category_id) & Q(instrument_type='future'), [], 'tq_factor')

                for index, cg_two in category_one.iterrows():
                    result[cg_one.category_name][cg_two.category_name] = dict()
                    for val in ['live', 'dead']:
                        result[cg_one.category_name][cg_two.category_name][val] = self.setFvCategoryField(Q(category2=cg_two.category_name) & Q(status=val))
        else:
            raise CommonException(400, 'type类型只有：table,category')
        return Response(result)

    def setFvTbleField(self, conditions):
        factor_df = FvFactorInfo.get_info_all(conditions, ['factor_name', 'status'], 'tq_factor')
        result = []
        if not factor_df.empty:
            factor_df.sort_values(by='factor_name', inplace=True, ascending=True)
            for key, val in factor_df.iterrows():
                result.append(val.loc['factor_name'])
        return result

    def setFvCategoryField(self, conditions):
        category_three = FvFactorInfo.get_info_all(conditions, ['factor_name', 'table_name'], 'tq_factor')
        table_info = []
        if not category_three.empty:
            # 找到重复值
            dup_factor = FvFactorInfo.get_distinct_field('factor_name', 'tq_factor')
            for key, val in category_three.iterrows():
                if val['factor_name'] in dup_factor:
                    factor_name = val['table_name'] + '.' + val['factor_name']
                else:
                    factor_name = val['factor_name']
                table_info.append(factor_name)
        return table_info


class FvScCalRankICIR(mixins.CreateModelMixin, viewsets.GenericViewSet):
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
        factor.stime = stime
        factor.etime = etime
        factor.diff = serializer.data['factor_diff']  # 因子差异
        factor.exchange = serializer.data['exchange_future']  # 交易所
        factor.periods = serializer.data['periods']  # 收益周期
        factor.correlation = serializer.data['correlation']  # 相关系数
        factor_service = FactorSingleTable(factor)
        result = factor_service.main(serializer.data['factor'])
        for t_name, t_val in result.items():
            temp_dict = dict()
            for l_name, l_data in cache.get(t_val)['summary'].items():
                temp_dict[l_name] = json.loads(cache.get(t_val)['summary'][l_name].T.to_json())
            result[t_name] = temp_dict
        return Response(result, status=status.HTTP_201_CREATED)
