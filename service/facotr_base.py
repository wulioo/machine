from abc import abstractmethod, ABCMeta

import pandas as pd
from django.db.models import Q, Model
from logs import logger
from extra.db.base_model import BaseModel
from extra.db.models_tqmain import FutureDominantDaily
from utils.exception import ResultEmpty


class FvFactorBase(metaclass=ABCMeta):
    stime: str
    etime: str
    column = None

    def get_main_contracts(self, factor_arr, type_name_ab, join_method='left'):
        """
        从 future_dominant_daily 获取日期品种的主力合约
        :param factor_arr:
        :param type_name_ab:
        :param join_method: 默认左连接
        :return:
        """
        fv_daily = FutureDominantDaily.get_orderby_info_all(
            Q(type_name_ab__in=type_name_ab) & Q(trading_date__range=[self.stime, self.etime]),
            ['trading_date', 'wind_code', 'type_name_ab'],
            ['type_name_ab', 'trading_date'], 'tqmain')
        if fv_daily.empty:
            raise ResultEmpty(400, msg=f'futere_dominant_daily 主力合约为空')
        factor_arr = factor_arr.merge(fv_daily, how=join_method, on=['trading_date', 'type_name_ab'])
        return factor_arr

    @abstractmethod
    def get_type_name(self):
        pass

    @abstractmethod
    def get_fv_factor(self):
        pass


class FvAnalysisBase(FvFactorBase):
    exchange = None
    model = None
    _db = 'tq_factor'

    def __init__(self):
        pass

    def set_db(self, val):
        self._db = val

    @property
    def get_type_name(self):
        """
        根据 交易所 表来获取type_name_ab
        :return:
        """
        df = self.model.get_duplication_field('type_name_ab', self._db)
        df['exchange'] = df['type_name_ab'].str[-3:]
        type_name_ab = df[df['exchange'].isin(self.exchange)]['type_name_ab'].tolist()

        return type_name_ab

    def get_fv_factor(self):
        df = self.model.get_orderby_info_all(Q(trading_date__range=[self.stime, self.etime]) & Q(type_name_ab__in=self.get_type_name),
                                             self.column + ['trading_date', 'type_name_ab'],
                                             ['type_name_ab', 'trading_date'], self._db)
        if df.empty:
            raise ResultEmpty(400, msg=f'{self.model._meta.db_table} 获取数据为空')
        return df

    @abstractmethod
    def cal_main(self):
        pass

    @abstractmethod
    def init_data_processing(self):
        pass


class FvReviewBase(FvFactorBase):
    def __init__(self, file_df: pd.DataFrame):
        self.df = file_df
        self.stime = str(file_df['trading_date'].min())
        self.etime = str(file_df['trading_date'].max())
        self.column = file_df.iloc[:, 2:].columns.tolist()

    @property
    def get_type_name(self):
        try:
            type_name_ab = self.df['type_name_ab'].unique().tolist()
        except KeyError as e:
            type_name_ab = self.df.iloc[:, 1].unique().tolist()
            logger.error('当前上传文件没有type_name_ab')
        return type_name_ab

    def get_fv_factor(self):
        pass

    @abstractmethod
    def cal_main(self):
        pass

    @abstractmethod
    def init_data_processing(self):
        pass
