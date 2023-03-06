import itertools
import json
import uuid
from datetime import datetime

import pandas as pd
from django.core.cache import cache
from django.db.models import Q

from apps.monitor.models import CmSeqIcIr
from apps.system.models import SysConf
from extra.db.models_tqfactor import FvFactorInfo
from extra.db.models_tqsignal import FvSignalInfo
from extra.factory.earnings import FvFactoryEarnings
from service.corr import CorrFactory
from service.earnings import Earnings
from service.facotr_base import FvReviewBase, FvAnalysisBase
from service.varieties import Varieties
from utils.common import Common, TimeContext
from apps.fv_sequential.tasks import sequential_ic
from celery.result import AsyncResult
from Machine.celery import app
from logs import logger
import numpy as np

from utils.config import SEQ_DATE_TIME, MONITOR_ICIR_TIME, FILE_SEQ_FAC_PATH, FILE_SEQ_SIG_PATH, SEQ_ADD_IC_FAC_THRESHOLD, SEQ_SUB_IC_FAC_THRESHOLD, SEQ_ADD_IR_FAC_THRESHOLD, SEQ_SUB_IR_FAC_THRESHOLD, \
    SEQ_ADD_IR_SIG_THRESHOLD, SEQ_SUB_IR_SIG_THRESHOLD, SEQ_SUB_IC_SIG_THRESHOLD, SEQ_ADD_IC_SIG_THRESHOLD
from utils.exception import ResultEmpty


class SequentialICIR:
    earn: Earnings
    periods: list
    column: list
    correlation: list
    windows: list
    interval: int = 0

    def celery_seq_ic(self, df: pd.DataFrame, types: list):
        # result = self.single_seq_ic(df, types)
        tps = Common.list_slice_by_core(types)
        with TimeContext('ICIR计算 cpu'):
            uuid_df = f"seq_df_{uuid.uuid1()}"
            cache.set(uuid_df, {'df': df, 'factor': self})
            corr_dfs = [sequential_ic.delay(uuid_df, t) for t in tps]
            result = {}
            for res in corr_dfs:
                async_result = AsyncResult(id=str(res), app=app)
                async_result.wait()  # 等待任务完
                result.update(async_result.get())
                async_result.forget()  # 将结果删除,执行完成，结果不会自动删除
            cache.delete(uuid_df)

        return result

    def single_seq_ic(self, df: pd.DataFrame, types: list):
        df = df.round(8)  # 避免相同的值排出不同名次
        df.set_index('trading_date', inplace=True)
        xs = self.column
        ys = [f'label_{y}' for y in self.periods]
        t_w_c_tuple = itertools.product(types, self.windows)
        result = dict()
        echarts = dict()
        for t, w in t_w_c_tuple:
            if not result.get(t):
                result[t] = dict()
                echarts[t] = dict()
            if not result[t].get(w):
                result[t][w] = dict()
                echarts[t][w] = dict()

            t_df = df.loc[df['type_name_ab'] == t, xs + ys].sort_index()
            if t_df.empty:
                logger.info(f'{t}:没有获取主力合约')
                continue
            if self.interval > 0:
                t_df[xs] = t_df[ys].shift(self.interval)
                t_df.dropna(subset=xs, inplace=True)
            for c in self.correlation:

                ic_corr = CorrFactory.create_Corr(c)
                ic_corr.xs = xs
                ic_corr.ys = ys
                if isinstance(w, int):
                    data = ic_corr.cal_rolling_ic(t_df, w)
                else:
                    data = ic_corr.cal_expanding_ic(t_df)

                if not result[t][w].get(c):
                    result[t][w][c] = dict()
                echarts[t][w][c] = data
                for l_name, label in data.items():
                    temp_dict = {}
                    if c == "spearman":
                        temp_dict['rank_ic_mean'] = label.mean()
                        temp_dict['rank_ir'] = label.mean() / label.std(ddof=0)
                    else:
                        temp_dict['normal_ic_mean'] = label.mean()
                        temp_dict['normal_ir'] = label.mean() / label.std(ddof=0)
                    summary = pd.DataFrame(temp_dict)
                    summary.index.rename('factor', inplace=True)
                    summary.reset_index(inplace=True)
                    result[t][w][c][l_name] = summary.round(4)
            if len(result[t][w]) > 1:

                result[t][w] = {key: result[t][w]['spearman'][key].merge(result[t][w]['pearson'][key], how="left", on='factor') for key in result[t][w]['spearman']}
            else:
                result[t][w] = list(result[t][w].values())[0]

        return self.resp_ml_data(result, echarts)

    def resp_ml_data(self, result, echarts):
        for t, val in result.items():
            for k_w, d_w in val.items():
                for k_l, d_l in d_w.items():
                    result[t][k_w][k_l] = list(json.loads(d_l.T.to_json()).values())
            key = uuid.uuid1()
            cache.set(key, val)
            cache.set(f'charts_{key}', echarts[t])
            result[t] = key
        return result


class FvSeqAnalysisICIR(FvAnalysisBase, SequentialICIR):
    vari: Varieties
    df: pd.DataFrame

    def init_data_processing(self):
        """数据预处理"""
        factor_arr = self.get_fv_factor()
        factor_arr = self.vari.fill_df_value(factor_arr, self.column)
        join_method = 'right' if self.vari.vits != "all" else 'left'
        factor_arr = self.get_main_contracts(factor_arr, self.get_type_name, join_method)
        factor_arr.dropna(subset=['wind_code'], inplace=True)
        return factor_arr

    def cal_main(self):
        wc_and_erg = self.earn.cal_earnings(self.df, self.periods)
        return self.celery_seq_ic(wc_and_erg, self.get_type_name)

    def resp_api_data(self, data):
        for key, val in data.items():
            data[key] = cache.get(val)
        return data


class FvSeqReviewICIR(FvReviewBase, SequentialICIR):

    def init_data_processing(self):
        factor_arr = self.get_main_contracts(self.df, self.get_type_name)
        factor_arr.dropna(subset=['wind_code'], inplace=True)
        return factor_arr

    def cal_main(self):
        factor_df = self.init_data_processing()
        wc_and_erg = self.earn.cal_earnings(factor_df, self.periods)
        return self.celery_seq_ic(wc_and_erg, self.get_type_name)


class FvSeqApiICIR(FvAnalysisBase, SequentialICIR):

    def init_data_processing(self):
        factor_arr = self.get_fv_factor()
        factor_arr = self.vari.fill_df_value(factor_arr, self.column)
        join_method = 'right' if self.vari.vits != "all" else 'left'
        factor_arr = self.get_main_contracts(factor_arr, self.get_type_name, join_method)
        factor_arr.dropna(subset=['wind_code'], inplace=True)
        return factor_arr

    def __init__(self, type_name_ab):
        self._type_name_ab = type_name_ab
        self.df: pd.DataFrame = pd.DataFrame(columns=['trading_date', 'type_name_ab', 'wind_code'])
        super().__init__()

    def cal_main(self):
        factor_df = self.earn.cal_earnings(self.df, self.periods)
        ic_data = self.single_seq_ic(factor_df, self.get_type_name)
        result = self.resp_api_data(ic_data)
        return result

    @property
    def get_type_name(self):
        return [self._type_name_ab]

    def resp_api_data(self, data):
        result = dict()
        for key, val in data.items():
            result = cache.get(val)
            break
        return result


class FvSeqMonitorICIR(FvAnalysisBase, SequentialICIR):
    df: pd.DataFrame
    etime = datetime.now().strftime("%Y-%m-%d")
    exchange = ['SHF', 'DCE', 'CZC', 'INE']
    periods = [1, 2, 3, 5, 10]
    windows = [60]
    correlation = ['spearman']

    def __init__(self):
        self._conf = SysConf.get_info_all(Q(model='monitor'), ['key', 'value'])
        self.stime = self._conf.loc[self._conf['key'] == "MONITOR_ICIR_TIME",'value'].iloc[0]
        self._date_time = self._conf.loc[self._conf['key'] == "SEQ_DATE_TIME",'value'].iloc[0]
        self._earn = FvFactoryEarnings().make_earnings(self.stime, self.etime, 'close_price')
        super().__init__()

    @property
    def get_info_model(self):
        if self._db == "tq_factor":
            return FvFactorInfo
        else:
            return FvSignalInfo

    @property
    def get_json_file(self):
        if self._db == "tq_factor":
            return FILE_SEQ_FAC_PATH
        else:
            return FILE_SEQ_SIG_PATH

    def init_data_processing(self):
        factor_arr = self.get_fv_factor()
        factor_df = self.get_main_contracts(factor_arr, self.get_type_name)
        factor_df.dropna(subset=['wind_code'], inplace=True)
        return factor_df

    def cal_main(self):
        wc_and_erg = self._earn.cal_earnings(self.df, self.periods)
        return self.celery_seq_ic(wc_and_erg, self.get_type_name)

    def _repeat_process(self, data, info_df):
        """重复因子查找表名"""
        df_nan = data[pd.isnull(data['table_name']) == True].iloc[:, :1]
        df_dup = info_df[info_df.groupby('factor_name')['factor_name'].transform('count') > 1]
        dup_list = df_dup.drop_duplicates(subset=['factor_name'], keep='first', inplace=False)['factor_name'].values
        dup_merger = pd.DataFrame(columns=['factor_name', 'table_name'])
        for factor in dup_list:
            df_temp = df_dup[df_dup['factor_name'] == factor]
            x_df = df_temp.iloc[:1, :]
            x_df['factor_name'] = x_df['factor_name'] + '_x'
            y_df = df_temp.iloc[1:2, :]
            y_df['factor_name'] = y_df['factor_name'] + '_y'
            dup_merger = dup_merger.merge(pd.concat([x_df, y_df]), how='outer', on=['factor_name', 'table_name'])
        df_res = df_nan.merge(dup_merger, how="left", on='factor_name')
        data.dropna(subset='table_name', inplace=True)
        factor_df = pd.concat([df_res, data], ignore_index=True)
        factor_df['factor_name'] = factor_df['factor_name'].str.replace("_y", "")
        factor_df['factor_name'] = factor_df['factor_name'].str.replace("_x", "")
        return factor_df

    def resp_ml_data(self, result, echarts):
        temp_res = dict()
        with open(self.get_json_file, "r") as f:
            _init_sec_data = json.loads(f.read())
        factor_info = self.get_info_model.get_info_all(None, ['factor_name', 'table_name'], self._db)

        for _t, t_data in result.items():
            temp_res[_t] = 'success'
            for _w, w_data in t_data.items():
                for _l, l_data in w_data.items():
                    l_data.set_index('factor', inplace=True)
                    try:
                        f_list = _init_sec_data[_t][str(self._date_time)][f'{_l[-1:]}']
                    except KeyError as e:
                        continue
                    factor_df = pd.DataFrame({'factor_name': f_list})
                    data = factor_info.merge(factor_df, how='right', on="factor_name")
                    data = self._repeat_process(data, factor_info)
                    if self._db == "tq_factor":
                        SEQ_ADD_IC_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_ADD_IC_FAC_THRESHOLD",'value'].iloc[0]
                        SEQ_ADD_IR_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_ADD_IR_FAC_THRESHOLD",'value'].iloc[0]
                        SEQ_SUB_IC_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_SUB_IC_FAC_THRESHOLD",'value'].iloc[0]
                        SEQ_SUB_IR_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_SUB_IR_FAC_THRESHOLD",'value'].iloc[0]
                    else:
                        SEQ_ADD_IC_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_ADD_IC_SIG_THRESHOLD",'value'].iloc[0]
                        SEQ_ADD_IR_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_ADD_IR_SIG_THRESHOLD",'value'].iloc[0]
                        SEQ_SUB_IC_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_SUB_IC_SIG_THRESHOLD",'value'].iloc[0]
                        SEQ_SUB_IR_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_SUB_IR_SIG_THRESHOLD",'value'].iloc[0]
                    data_ok = l_data.loc[(abs(l_data['rank_ic_mean']) > float(SEQ_ADD_IC_THRESHOLD)) & (abs(l_data['rank_ir']) > float(SEQ_ADD_IR_THRESHOLD)), ['rank_ic_mean', 'rank_ir']]
                    data_exit = l_data.loc[(abs(l_data['rank_ic_mean']) < float(SEQ_SUB_IC_THRESHOLD)) & (abs(l_data['rank_ir']) < float(SEQ_SUB_IR_THRESHOLD)), ['rank_ic_mean', 'rank_ir']]
                    if not data_ok.empty:
                        data_ok.apply(lambda x: self._entry_ok(x, data, _t, _w, _l), axis=1)
                    if not data_exit.empty:
                        data_exit.apply(lambda x: self._entry_exit(x, data, _t, _w, _l), axis=1)
        return temp_res

    def _entry_ok(self, val, init_json_data, type_name_ab, windows, label):
        ic = round(val['rank_ic_mean'], 4)
        ir = round(val['rank_ir'], 4)
        table_name = self.model._meta.db_table
        factor_name = val.name
        base_table = init_json_data[(init_json_data['table_name'] == table_name) & (init_json_data['factor_name'] == factor_name)]
        factor_info = CmSeqIcIr.objects.filter(Q(table=table_name) & Q(factor=factor_name) & Q(label=label) & Q(type_name_ab=type_name_ab) & Q(windows=windows) & Q(database=self._db)).first()
        if not factor_info:
            CmSeqIcIr.objects.create(
                type_name_ab=type_name_ab,
                table=table_name,
                factor=factor_name,
                rank_ic=ic,
                rank_ir=ir,
                label=label,
                status=3,
                remark='',
                windows=windows,
                update_time=datetime.now(),
                create_time=datetime.now(),
                database=self._db
            )
        factor_info = CmSeqIcIr.objects.filter(Q(table=table_name) & Q(factor=factor_name) & Q(label=label) & Q(type_name_ab=type_name_ab) & Q(windows=windows) & Q(database=self._db)).first()
        if base_table.empty:
            factor_info.status = 0  # 0:不在基准因子池中
            factor_info.remark = '纳入'  # 不在基准因子池中 纳入新增进来的
            factor_info.rank_ic = ic
            factor_info.rank_ir = ir
            factor_info.update_time = datetime.now()
            factor_info.save()
        else:
            factor_info.status = 1  # 1:在基准因子池中
            factor_info.remark = ''  # 在基准因子池中为 空
            factor_info.rank_ic = ic
            factor_info.rank_ir = ir
            factor_info.update_time = datetime.now()
            factor_info.save()

    def _entry_exit(self, val, init_json_data, type_name_ab, windows, label):
        ic = round(val['rank_ic_mean'], 4)
        ir = round(val['rank_ir'], 4)
        table_name = self.model._meta.db_table
        factor_name = val.name
        base_table = init_json_data[(init_json_data['table_name'] == table_name) & (init_json_data['factor_name'] == factor_name)]
        factor_info = CmSeqIcIr.objects.filter(Q(table=table_name) & Q(factor=factor_name) & Q(label=label) & Q(type_name_ab=type_name_ab) & Q(windows=windows) & Q(database=self._db)).first()
        if base_table.empty:
            if factor_info:
                factor_info.remark = ''
                factor_info.rank_ic = ic
                factor_info.rank_ir = ir
                factor_info.update_time = datetime.now()
                factor_info.create_time = datetime.now()
                factor_info.save()
        else:
            if factor_info:
                factor_info.remark = '剔除'
                factor_info.rank_ic = ic
                factor_info.rank_ir = ir
                factor_info.update_time = datetime.now()
                factor_info.save()
            else:
                CmSeqIcIr.objects.create(
                    type_name_ab=type_name_ab,
                    table=table_name,
                    factor=factor_name,
                    rank_ic=ic,
                    rank_ir=ir,
                    label=label,
                    status=1,
                    remark='剔除',
                    windows=windows,
                    update_time=datetime.now(),
                    create_time=datetime.now(),
                    database=self._db
                )
