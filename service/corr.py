from abc import ABCMeta, abstractmethod
import pandas as pd
import numpy as np
from django.core.cache import cache
from numpy.lib.stride_tricks import as_strided
from numpy.lib import pad
import uuid
from logs import logger


class CorrFactory:
    @staticmethod
    def create_Corr(correlation):
        if correlation == 'pearson':
            return Pearson()
        elif correlation == 'spearman':
            return Spearman()


class Corr(metaclass=ABCMeta):
    _xs = None
    _ys = None

    @property
    def xs(self):
        return self._xs

    @xs.setter
    def xs(self, xs) -> None:
        self._xs = xs

    @property
    def ys(self):
        return self._ys

    @ys.setter
    def ys(self, ys) -> None:
        self._ys = ys

    @abstractmethod
    def cal_rolling_ic(self, df: pd.DataFrame, window: int):
        pass

    @abstractmethod
    def cal_expanding_ic(self, df: pd.DataFrame):
        pass


class Pearson(Corr):
    def cal_rolling_ic(self, df: pd.DataFrame, window: int):
        pearson = df[self._xs].rolling(window).corr(df[self._ys], pairwise=True)
        pearson.where(pearson.abs() <= 1, np.nan, inplace=True)
        pearson.reset_index(level=0, inplace=True)
        result = {}
        for y in self._ys:

            result[y] = pearson.loc[y].set_index("trading_date")

        return result

    def cal_expanding_ic(self, df: pd.DataFrame):
        pearson = df[self._xs].expanding(480).corr(df[self._ys], pairwise=True)
        pearson.where(pearson.abs() <= 1, np.nan, inplace=True)
        pearson.reset_index(level=0, inplace=True)
        result = {}
        for y in self._ys:
            result[y] = pearson.loc[y].set_index("trading_date")

        return result


class Spearman(Corr):
    def cal_rolling_ic(self, df: pd.DataFrame, window: int):
        """
        reference: https://www.coder.work/article/1277954
        pod作用: https://blog.csdn.net/codetypeman/article/details/90454153
        """
        result = {}
        if len(df) < window:  # 数据长度小于窗口期，直接返回空值
            for y in self._ys:
                result[y] = pd.DataFrame(index=df.index, columns=self._xs)
        else:
            matrix_dict = {}
            for col in self._xs + self._ys:
                matrix_dict[col] = self.__rolling_matrix_ranked(df[col], window)
            for y in self._ys:
                y_spearman = pd.DataFrame(index=df.index)
                for x in self._xs:
                    corrs = matrix_dict[x].corrwith(matrix_dict[y], axis=1)
                    y_spearman[x] = pad(corrs, (window - 1, 0), 'constant', constant_values=np.nan)
                y_spearman.where(y_spearman.abs() <= 1, np.nan, inplace=True)
                result[y] = y_spearman
        return result

    def cal_expanding_ic(self, df: pd.DataFrame):
        result = {}
        for y in self._ys:
            y_spearman = pd.DataFrame(index=df.index)
            for x in self._xs:
                y_spearman[x] = df[x].expanding(480).apply(lambda x: self.__spearman_corr(x, df[y]))
            y_spearman.where(y_spearman.abs() <= 1, np.nan, inplace=True)
            result[y] = y_spearman
        return result

    def __rolling_matrix_ranked(self, s: pd.Series, window: int):
        s = s.values
        stride = s.strides[0]
        matrix = as_strided(s, shape=[len(s) - window + 1, window], strides=[stride, stride])
        matrix = pd.DataFrame(matrix).copy()
        matrix[matrix.isna().any(axis=1)] = np.nan
        matrix = matrix.rank(axis=1)
        return matrix

    def __spearman_corr(self, s1: pd.Series, s2: pd.Series):
        s2 = s2.loc[s1.index]
        return s1.corr(s2, method='spearman')
