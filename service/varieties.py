from abc import ABCMeta, abstractmethod

import pandas as pd
from typing import List, Dict


class VarietiesFactory:
    @staticmethod
    def create_varieties(vits_fun):
        if vits_fun == 'mean':
            return VarietiesMedian()
        elif vits_fun == 'median':
            return VarietiesMean()
        elif vits_fun == 'zero':
            return VarietiesZero()
        elif vits_fun == 'all':
            return VarietiesAll()


class Varieties(metaclass=ABCMeta):
    vits = None
    @abstractmethod
    def fill_df_value(self, df: pd.DataFrame, cols: list):
        pass


class VarietiesMedian(Varieties):
    vits = 'median'

    def fill_df_value(self, df: pd.DataFrame, cols: list):
        """各日期截面用中位数填充空值"""
        tds = df['trading_date'].unique().tolist()
        for td in tds:
            if not df.loc[df['trading_date'] == td, cols].isna().any().any():
                continue
            df.loc[df['trading_date'] == td, cols] = df.loc[df['trading_date'] == td, cols].fillna(
                df.loc[df['trading_date'] == td, cols].quantile())
        return df


class VarietiesMean(Varieties):
    vits = 'mean'

    def fill_df_value(self, df: pd.DataFrame, cols: list):
        """各日期截面用均值填充空值"""
        tds = df['trading_date'].unique().tolist()
        for td in tds:
            if not df.loc[df['trading_date'] == td, cols].isna().any().any():
                continue
            df.loc[df['trading_date'] == td, cols] = df.loc[df['trading_date'] == td, cols].fillna(
                df.loc[df['trading_date'] == td, cols].mean())
        return df


class VarietiesZero(Varieties):
    vits = 'zero'

    def fill_df_value(self, df: pd.DataFrame, cols: list):
        """各日期截面用0填充空值"""
        df.loc[:, cols] = df.loc[:, cols].fillna(0)
        return df


class VarietiesAll(Varieties):
    vits = 'all'

    def fill_df_value(self, df: pd.DataFrame, cols: list):
        """不做处理"""
        return df
