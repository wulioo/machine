import json
import os
import uuid
from abc import abstractmethod
from datetime import datetime

import pandas as pd
from django.core.cache import cache
from django.db.models import Q, Model
from redis.exceptions import InvalidResponse

from Machine.celery import app
from celery.result import AsyncResult
import numpy as np
from Machine.settings import PROCESS_NUM, BASE_DIR
from apps.monitor.models import CmSecIcIr
from apps.system.models import SysConf
from extra.db.base_model import BaseModel
from extra.db.models_tqfactor import FvFactorInfo
from extra.db.models_tqsignal import FvSignalInfo
from extra.factory.earnings import FvFactoryEarnings
from service.avg_earnings import FvSecAvgEarnings
from service.axis import AxisMixin, AxisMixin
from service.earnings import Earnings
from service.facotr_base import FvAnalysisBase, FvReviewBase
from service.factor import Factor, EquityFactor, FutureFactor
from service.night import NightTrading
from service.sort import SortMixin
from service.varieties import Varieties, VarietiesAll
from utils.common import TimeContext, Common, func_time
from apps.future.tasks import celery_ic, celery_factor_diff, celery_factor_eq_diff
from utils.config import MONITOR_ICIR_TIME, FILE_SEC_FAC_PATH, FILE_SEC_SIG_PATH, SEC_ADD_IC_FAC_THRESHOLD, SEC_SUB_IC_SIG_THRESHOLD, SEC_ADD_IR_FAC_THRESHOLD, SEC_SUB_IR_FAC_THRESHOLD, \
    SEC_SUB_IC_FAC_THRESHOLD, SEC_ADD_IC_SIG_THRESHOLD, SEC_ADD_IR_SIG_THRESHOLD, SEC_SUB_IR_SIG_THRESHOLD
from utils.exception import CommonException


class SectionICIR(SortMixin, AxisMixin):
    periods = None
    correlation = None
    diff = None
    vari: Varieties
    earn: Earnings

    def _cal_rank_normal_ic(self, df):
        """
       定义特征、标签、日期
       celery版本
       :param df:
       :return:
       """
        df['trading_date'] = df['trading_date'].astype(str)
        tds = sorted(df['trading_date'].unique().tolist())

        # 1.计算 Normal Rink IC pearson spearman
        with TimeContext(f'ic计算 cpu'):
            tds = Common.list_slice_by_core(tds)
            uuid_df = f"ic_df_{uuid.uuid1()}"
            cache.set(uuid_df, {
                'df': df,
                'factor': self
            })
            corr_dfs = [celery_ic.delay(td, uuid_df) for td in tds]
            result = {corr: pd.DataFrame() for corr in self.correlation}
            for res in corr_dfs:
                async_result = AsyncResult(id=str(res), app=app)
                async_result.wait()
                corr_json = async_result.get()
                for corr in self.correlation:
                    corr_df = pd.read_json(corr_json[corr], encoding="utf-8", orient='records')
                    result[corr] = pd.concat([corr_df, result[corr]], ignore_index=True)
                async_result.forget()  # 将结果删除,执行完成，结果不会自动删除

            cache.delete(uuid_df)

            data = {}
            for n_corr, corr in result.items():
                corr.set_index('trading_date', inplace=True)
                # 2.将数据拼接字典格式加到data里面
                data[n_corr] = {}
                for y in self.ys:
                    y_corr = corr[corr['label'] == y]
                    y_corr.drop(columns='label', inplace=True)
                    data[n_corr][y] = y_corr
        return data

    def cal_single_rank_normal_ic(self, df, tds):
        corr_dfs = {cor: [] for cor in self.correlation}
        for td in tds:
            for cor in self.correlation:
                td_df = df[df['trading_date'] == td]
                corr = td_df[self.xy].corr(method=cor).loc[self.ys, self.xs]
                corr.index.rename('label', inplace=True)
                corr.reset_index(inplace=True)
                corr['trading_date'] = td
                corr_dfs[cor].append(corr)

        for cor in self.correlation:
            corr_dfs[cor] = pd.concat(corr_dfs[cor], ignore_index=True).to_json()
        return corr_dfs

    def _summary(self, return_mean, ic):
        data = {}
        with TimeContext('结果汇总计算 cpu'):
            # xy, xs, ys = y_x_xy
            for y in self.ys:
                y_df = pd.DataFrame(index=self.xs)
                try:
                    y_df['return_mean'] = return_mean[y].mean() / int(y.split("_")[1])
                except AttributeError as e:
                    for key, val in return_mean[y].items():
                        y_df[key] = val.mean() / int(y.split("_")[1])
                except TypeError:
                    pass
                if 'pearson' in self.correlation:
                    y_df['normal_IC_mean'] = ic['pearson'][y].mean()
                    y_df['normal_IC_std'] = ic['pearson'][y].std(ddof=0)
                    y_df['normal_IC>2%'] = (ic['pearson'][y] > 0.02).sum() / ic['pearson'][y].count()
                    y_df['normal_IC<-2%'] = (ic['pearson'][y] < -0.02).sum() / ic['pearson'][y].count()
                    y_df['normal_IR'] = y_df['normal_IC_mean'] / y_df['normal_IC_std']

                if 'spearman' in self.correlation:
                    y_df['rank_IC_mean'] = ic['spearman'][y].mean()
                    y_df['rank_IC_std'] = ic['spearman'][y].std(ddof=0)
                    y_df['rank_IC>2%'] = (ic['spearman'][y] > 0.02).sum() / ic['spearman'][y].count()
                    y_df['rank_IC<-2%'] = (ic['spearman'][y] < -0.02).sum() / ic['spearman'][y].count()
                    y_df['rank_IR'] = y_df['rank_IC_mean'] / y_df['rank_IC_std']

                y_df.index.rename('factors', inplace=True)
                data[y] = y_df
        return data

    def _save_redis(self, data):
        """
        数据格式转换并且保存至redis
        """
        uuid_df = uuid.uuid1()
        cache.set(str(uuid_df), data)
        return uuid_df


class FvSecAnalysisICIR(FvAnalysisBase, SectionICIR, NightTrading):
    df: pd.DataFrame

    def init_data_processing(self):
        """数据预处理"""
        factor_df = self.get_fv_factor()
        factor_df = self.get_night_trading_type(factor_df) if self.night else factor_df
        factor_df = self.vari.fill_df_value(factor_df, self.column)
        factor_df = self.get_factor_sort(factor_df) if self.sort else factor_df
        join_method = 'right' if self.vari.vits != "all" else 'left'
        factor_df = self.get_main_contracts(factor_df, self.get_type_name, join_method)
        factor_df.dropna(subset=['wind_code'], inplace=True)
        return factor_df

    def cal_main(self):
        wc_and_erg = self.earn.cal_earnings(self.df, self.periods)
        self.get_y_x_xy(wc_and_erg, self.column, self.periods)
        ic = self._cal_rank_normal_ic(wc_and_erg)
        avg_obj = FvSecAvgEarnings(self.xs, self.ys)
        if self.diff:
            avg_obj.cal_celery_return_mean(wc_and_erg, self.diff)
        data = self._summary(avg_obj.return_mean, ic)
        ic.update({'summary': data})
        result = self._resp_data(ic)
        return result

    def _resp_data(self, data):
        return self._save_redis(data)


class FvSecMonitorICIR(FvAnalysisBase, SectionICIR, NightTrading):
    df: pd.DataFrame
    etime = datetime.now().strftime("%Y-%m-%d")
    exchange = ['SHF', 'DCE', 'CZC', 'INE']
    periods = [1, 2, 3, 5, 10]
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
            return FILE_SEC_FAC_PATH
        else:
            return FILE_SEC_SIG_PATH

    def init_data_processing(self):
        """数据预处理"""
        factor_df = self.get_fv_factor()
        factor_df = self.get_night_trading_type(factor_df) if self.night else factor_df
        factor_df = self.get_main_contracts(factor_df, self.get_type_name)
        factor_df.dropna(subset=['wind_code'], inplace=True)
        return factor_df

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

    def cal_main(self, SEC_SUB_IR__SIG_THRESHOLD=None):
        wc_and_erg = self._earn.cal_earnings(self.df, self.periods)
        self.get_y_x_xy(wc_and_erg, self.column, self.periods)
        ic = self._cal_rank_normal_ic(wc_and_erg)
        data = self._summary(None, ic)
        with open(self.get_json_file, "r") as f:
            _init_sec_data = json.loads(f.read())

        factor_info = self.get_info_model.get_info_all(None, ['factor_name', 'table_name'], self._db)
        for _l, l_data in data.items():
            try:
                f_list = _init_sec_data[f'{_l[-1:]}']
            except KeyError as e:
                continue
            factor_df = pd.DataFrame({'factor_name': f_list})
            data = factor_info.merge(factor_df, how='right', on="factor_name")
            data = self._repeat_process(data, factor_info)
            if self._db == "tq_factor":
                SEQ_ADD_IC_THRESHOLD = self._conf.loc[self._conf['key'] == "SEC_ADD_IC_FAC_THRESHOLD", 'value'].iloc[0]
                SEQ_ADD_IR_THRESHOLD = self._conf.loc[self._conf['key'] == "SEC_ADD_IR_FAC_THRESHOLD", 'value'].iloc[0]
                SEQ_SUB_IC_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_SUB_IC_FAC_THRESHOLD", 'value'].iloc[0]
                SEQ_SUB_IR_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_SUB_IR_FAC_THRESHOLD", 'value'].iloc[0]
            else:
                SEQ_ADD_IC_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_ADD_IC_SIG_THRESHOLD", 'value'].iloc[0]
                SEQ_ADD_IR_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_ADD_IR_SIG_THRESHOLD", 'value'].iloc[0]
                SEQ_SUB_IC_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_SUB_IC_SIG_THRESHOLD", 'value'].iloc[0]
                SEQ_SUB_IR_THRESHOLD = self._conf.loc[self._conf['key'] == "SEQ_SUB_IR_SIG_THRESHOLD", 'value'].iloc[0]

            data_ok = l_data.loc[(abs(l_data['rank_IC_mean']) > float(SEQ_ADD_IC_THRESHOLD)) & (abs(l_data['rank_IR']) > float(SEQ_ADD_IR_THRESHOLD)), ['rank_IC_mean', 'rank_IR']]
            data_exit = l_data.loc[(abs(l_data['rank_IC_mean']) < float(SEQ_SUB_IC_THRESHOLD)) & (abs(l_data['rank_IR']) < float(SEQ_SUB_IC_THRESHOLD)), ['rank_IC_mean', 'rank_IR']]
            if not data_ok.empty:
                data_ok.apply(lambda x: self._entry_ok(x, data, _l), axis=1)
            if not data_exit.empty:
                data_exit.apply(lambda x: self._entry_exit(x, data, _l), axis=1)

        return 'success'


    def _entry_ok(self, val, init_json_data, label):
        ic = round(val['rank_IC_mean'], 4)
        ir = round(val['rank_IR'], 4)
        table_name = self.model._meta.db_table
        factor_name = val.name
        base_table = init_json_data[(init_json_data['table_name'] == table_name) & (init_json_data['factor_name'] == factor_name)]
        factor_info = CmSecIcIr.objects.filter(Q(table=table_name) & Q(factor=factor_name) & Q(label=label) & Q(is_night=int(self.night)) & Q(database=self._db)).first()
        if not factor_info:
            CmSecIcIr.objects.create(
                table=table_name,
                factor=factor_name,
                rank_ic=ic,
                rank_ir=ir,
                label=label,
                status=3,
                remark='',
                is_night=int(self.night),
                update_time=datetime.now(),
                create_time=datetime.now(),
                database=self._db

            )
        factor_info = CmSecIcIr.objects.filter(Q(table=table_name) & Q(factor=factor_name) & Q(label=label) & Q(is_night=int(self.night)) & Q(database=self._db)).first()

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

    def _entry_exit(self, val, init_json_data, label):
        ic = round(val['rank_IC_mean'], 4)
        ir = round(val['rank_IR'], 4)
        table_name = self.model._meta.db_table
        factor_name = val.name
        base_table = init_json_data[(init_json_data['table_name'] == table_name) & (init_json_data['factor_name'] == factor_name)]
        factor_info = CmSecIcIr.objects.filter(Q(table=table_name) & Q(factor=factor_name) & Q(label=label) & Q(is_night=int(self.night)) & Q(database=self._db)).first()
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
                # if factor_info.status == 1:
                #     factor_info.remark = '剔除'
                # else:
                #     factor_info.remark = ''
                factor_info.remark = '剔除'
                factor_info.rank_ic = ic
                factor_info.rank_ir = ir
                factor_info.update_time = datetime.now()
                factor_info.save()
            else:
                CmSecIcIr.objects.create(
                    table=table_name,
                    factor=factor_name,
                    rank_ic=ic,
                    rank_ir=ir,
                    label=label,
                    status=1,
                    remark='剔除',
                    is_night=int(self.night),
                    update_time=datetime.now(),
                    create_time=datetime.now(),
                    database=self._db
                )

    # def cal_main(self):
    #     wc_and_erg = self.earn.cal_earnings(self.df, self.periods)
    #     self.get_y_x_xy(wc_and_erg, self.column, self.periods)
    #     ic = self._cal_rank_normal_ic(wc_and_erg)
    #     data = self._summary(None, ic)
    #     for _l, l_data in data.items():
    #         data_ok = l_data.loc[(abs(l_data['rank_IC_mean']) > SEC_ADD_IC_THRESHOLD) & (abs(l_data['rank_IR']) > SEC_ADD_IR_THRESHOLD), ['rank_IC_mean', 'rank_IR']]
    #         data_exit = l_data.loc[(abs(l_data['rank_IC_mean']) < SEC_SUB_IC_THRESHOLD) & (abs(l_data['rank_IR']) < SEC_SUB_IR_THRESHOLD), ['rank_IC_mean', 'rank_IR']]
    #
    #         if not data_ok.empty:
    #             data_ok.apply(lambda x: self._entry_ok(x, _l), axis=1)
    #         if not data_exit.empty:
    #             data_exit.apply(lambda x: self._entry_exit(x, _l), axis=1)
    #
    #     return 'success'

    # def _entry_ok(self, data, label):
    #     table = self.model._meta.db_table
    #     factor = data.name
    #     factor_info = CmSecIcIr.objects.filter(Q(table=table) & Q(factor=factor) & Q(label=label) & Q(is_night=int(self.night))).first()
    #     if not factor_info:
    #         cm_ic_ir = CmSecIcIr.objects.create(
    #             table=table,
    #             factor=factor,
    #             rank_ic=data['rank_IC_mean'],
    #             rank_ir=data['rank_IR'],
    #             label=label,
    #             status=0,
    #             remark='纳入',
    #             is_night=int(self.night),
    #             update_time=datetime.now(),
    #             create_time=datetime.now(),
    #         )
    #     else:
    #         factor_info.remark = '纳入'
    #         factor_info.rank_ic = data['rank_IC_mean']
    #         factor_info.rank_ir = data['rank_IR']
    #         factor_info.update_time = datetime.now()
    #         factor_info.save()

    # def _entry_exit(self, data, label):
    #     table = self.model._meta.db_table
    #     factor = data.name
    #     factor_info = CmSecIcIr.objects.filter(Q(table=table) & Q(factor=factor) & Q(label=label) & Q(is_night=int(self.night))).first()
    #     if factor_info:
    #         factor_info.remark = '剔除'
    #         factor_info.rank_ic = data['rank_IC_mean']
    #         factor_info.rank_ir = data['rank_IR']
    #         # factor_info.status = 0
    #         factor_info.update_time = datetime.now()
    #         factor_info.create_time = datetime.now()
    #         factor_info.save()


class FvSecOneReviewICIR(FvReviewBase, SectionICIR):

    def init_data_processing(self):
        factor_df = self.get_factor_sort(self.df) if self.sort else self.df
        factor_arr = self.get_main_contracts(factor_df, self.get_type_name)
        factor_arr.dropna(subset=['wind_code'], inplace=True)
        return factor_arr

    def cal_main(self):
        factor_df = self.init_data_processing()
        wc_and_erg = self.earn.cal_earnings(factor_df, self.periods)
        self.get_y_x_xy(wc_and_erg, self.column, self.periods)
        ic = self._cal_rank_normal_ic(wc_and_erg)
        avg_obj = FvSecAvgEarnings(self.xs, self.ys)
        if self.diff:
            # wc_and_erg['wind_code'] = wc_and_erg['spread_name']
            avg_obj.cal_celery_return_mean(wc_and_erg, self.diff)
        data = self._summary(avg_obj.return_mean, ic)
        ic.update({'summary': data})
        result = self._save_redis(ic)
        return result


class FvSecTwoReviewICIR(FvReviewBase, SectionICIR):

    def __init__(self, file_df: pd.DataFrame, file_price: pd.DataFrame):
        self.file_price = file_price
        super(FvSecTwoReviewICIR, self).__init__(file_df)

    def init_data_processing(self):
        pass

    def cal_main(self):
        wc_and_erg = self.earn.cal_file_earnings(self.df, self.file_price, self.periods)
        self.get_y_x_xy(wc_and_erg, self.column, self.periods)
        ic = self._cal_rank_normal_ic(wc_and_erg)
        avg_obj = FvSecAvgEarnings(self.xs, self.ys)
        if self.diff:
            avg_obj.cal_celery_return_mean(wc_and_erg, self.diff)
        data = self._summary(avg_obj.return_mean, ic)
        ic.update({'summary': data})
        result = self._save_redis(ic)
        return result


class EqFactorICIR(EquityFactor, SectionICIR):

    def _cal_single_return_mean(self, df, ys, xs, tds):
        pass

    def _cal_return_mean(self, df, xy_xs_ys, diff=None):
        """
        celery版本 标签版本
        看因子排前20%的收益率比因子排后20%的收益率多多少,
        类似于分层测试第一层比最后一层多多少,
        类似于分层测试第一层比最后一层多多少
        :param df:
        :param xy_xs_ys:
        :param diff
        :return:
        """
        xy, xs, ys = xy_xs_ys
        df['trading_date'] = df['trading_date'].astype(str)
        tds = sorted(df['trading_date'].unique().tolist())
        tds = Common.list_slice_by_core(tds)
        factor_diff = {}
        with TimeContext(f'因子差异计算 cpu'):
            uuid_df = f"factor_diff_{uuid.uuid1()}"
            cache.set(uuid_df, df)
            for y in ys:
                factor_diff[y] = {}
                result = [celery_factor_eq_diff.delay(uuid_df, td, y, xs, diff) for td in tds]
                data = {val: [] for val in diff}
                for res in result:
                    async_result = AsyncResult(id=str(res), app=app)
                    async_result.wait()  # 等待任务完
                    return_mean = async_result.get()
                    for key, val in return_mean.items():
                        factor_df = pd.read_json(val, encoding="utf-8", orient='records')
                        data[key].append(factor_df)
                    async_result.forget()
                for key, val in data.items():
                    factor_diff[y][key] = pd.concat(val)
            cache.delete(uuid_df)
        return factor_diff
