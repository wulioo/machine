import uuid
from abc import ABCMeta, abstractmethod
from Machine.celery import app
from celery.result import AsyncResult
import pandas as pd
from django.core.cache import cache
from apps.future.tasks import celery_factor_diff

from utils.common import TimeContext, Common


class AvgEarnings(metaclass=ABCMeta):

    def __init__(self, xs, ys):
        self.xs = xs
        self.ys = ys
        self.return_mean = None

    @abstractmethod
    def cal_single_return_mean(self, df, tds, y):
        pass

    @abstractmethod
    def cal_celery_return_mean(self, df, diff=None):
        pass


class FvSecAvgEarnings(AvgEarnings):
    def cal_single_return_mean(self, df, tds, y):
        return_df = pd.DataFrame(index=tds, columns=self.xs)
        cls = df.drop(labels=self.xs+self.ys, axis=1).columns.tolist()
        for td in tds:
            td_df = df[df['trading_date'] == td]
            for x in self.xs:
                x_df = td_df[[x, y, cls[1]]]
                x_df.dropna(subset=[x, y], inplace=True)
                instr_per_group = round(len(x_df) / 5)
                if instr_per_group == 0:
                    continue
                x_df.sort_values(by=[x, cls[1]], ascending=[False, True], inplace=True, ignore_index=True)

                return_df.loc[td, x] = x_df[y].iloc[:instr_per_group].mean() - x_df[y].iloc[-instr_per_group:].mean()
        return_df.index.rename('trading_date', inplace=True)
        return return_df

    def cal_celery_return_mean(self, df, diff=None):
        """
        celery版本 标签版本
        看因子排前20%的收益率比因子排后20%的收益率多多少,
        类似于分层测试第一层比最后一层多多少,
        :param df:
        :param xy_xs_ys:
        :param diff
        :return:
        """
        df['trading_date'] = df['trading_date'].astype(str)
        tds = sorted(df['trading_date'].unique().tolist())

        with TimeContext(f'因子差异计算 cpu'):
            tds = Common.list_slice_by_core(tds)
            uuid_df = f"factor_diff_{uuid.uuid1()}"
            cache.set(uuid_df, {'df': df, 'factor': self})
            factor_diff = {}
            for y in self.ys:
                # self.cal_single_return_mean(df, tds, y)
                result = [celery_factor_diff.delay(uuid_df, td, y) for td in tds]
                data = []
                for res in result:
                    async_result = AsyncResult(id=str(res), app=app)
                    async_result.wait()  # 等待任务完
                    data.append(pd.read_json(async_result.get(), encoding="utf-8", orient='records'))
                    async_result.forget()
                factor_diff[y] = pd.concat(data)
            cache.delete(uuid_df)
        self.return_mean = factor_diff
        # return factor_diff
