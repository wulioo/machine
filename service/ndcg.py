import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')


class Ndcg:
    def __init__(self, n_group: int, factor_col: str, erg_col: str):
        self.__n_group = n_group
        self.__factor_col = factor_col
        self.__erg_col = erg_col
        self.data = {}

    # @func_time
    def __cal_td_ndcg(self, td_df: pd.DataFrame) -> (float, float):
        """计算一个交易日的多空头 ndcg"""

        # 计算当天每层 instrument 个数，多空头收益率减去最小值转为非负数
        instr_per_group = len(td_df) / self.__n_group
        td_df[f'{self.__erg_col}_long'] = td_df[self.__erg_col] - td_df[self.__erg_col].min()
        td_df[f'{self.__erg_col}_short'] = - td_df[self.__erg_col] - (-td_df[self.__erg_col]).min()


        # 多头、空头收益率按因子值降序、自降序排列
        label_long = td_df.sort_values(by=self.__factor_col, ascending=False, ignore_index=True)[
            f'{self.__erg_col}_long']
        label_long_ideal = td_df[f'{self.__erg_col}_long'].sort_values(ascending=False, ignore_index=True)
        label_short = td_df.sort_values(by=self.__factor_col, ascending=False, ignore_index=True)[
            f'{self.__erg_col}_short']
        label_short_ideal = td_df[f'{self.__erg_col}_short'].sort_values(ascending=False, ignore_index=True)
        # 计算各层折损和平均收益率
        group_df = pd.DataFrame(columns=['discount', 'long', 'long_ideal', 'short', 'short_ideal'])
        for i in range(self.__n_group):
            group_df.loc[i, 'discount'] = np.log2(i + 1 + 1)
            index_start = round(i * instr_per_group)
            index_end = round((i + 1) * instr_per_group)
            group_df.loc[i, 'long'] = label_long.iloc[index_start:index_end].mean()
            group_df.loc[i, 'long_ideal'] = label_long_ideal.iloc[index_start:index_end].mean()
            group_df.loc[i, 'short'] = label_short.iloc[index_start:index_end].mean()
            group_df.loc[i, 'short_ideal'] = label_short_ideal.iloc[index_start:index_end].mean()

        # 计算 dcg 和 idcg
        dcg_long = (group_df['long'] / group_df['discount']).sum()
        idcg_long = (group_df['long_ideal'] / group_df['discount']).sum()
        dcg_short = (group_df['short'] / group_df['discount']).sum()
        idcg_short = (group_df['short_ideal'] / group_df['discount']).sum()

        # 计算 ndcg
        if idcg_long == 0:
            td_ndcg_long = np.nan
        else:
            td_ndcg_long = dcg_long / idcg_long

        if idcg_short == 0:
            td_ndcg_short = np.nan
        else:
            td_ndcg_short = dcg_short / idcg_short

        return td_ndcg_long, td_ndcg_short

    # @func_time
    def calculate_ndcg(self, df):
        """
        指定层数、因子、标签、起止日期，计算日均多空头
        :param df:
        """
        # drop 掉因子或标签为空的行

        df_no_nan = df.dropna(subset=[self.__factor_col, self.__erg_col])

        # 初始化以 trading_date 为 index 的 ndcg_df
        tds = sorted(df_no_nan['trading_date'].unique().tolist())
        ndcg_df = pd.DataFrame(index=tds, columns=['ndcg_long', 'ndcg_short'])

        # 对每个交易日计算多空头 ndcg
        for td in tds:
            td_df = df_no_nan[df_no_nan['trading_date'] == td]
            td_ndcg_long, td_ndcg_short = self.__cal_td_ndcg(td_df)
            ndcg_df.loc[td, 'ndcg_long'] = td_ndcg_long
            ndcg_df.loc[td, 'ndcg_short'] = td_ndcg_short

        # 计算日均 ndcg
        self.data['avg_ndcg_long'] = ndcg_df['ndcg_long'].mean()
        self.data['avg_ndcg_short'] = ndcg_df['ndcg_short'].mean()
        self.data = pd.DataFrame(self.data, index=[self.__factor_col])

    def celery_ndcg(self, df_no_nan, tds):
        """
        指定层数、因子、标签、起止日期，计算日均多空头
        :param df:
        """


        # 初始化以 trading_date 为 index 的 ndcg_df
        ndcg_df = pd.DataFrame(index=tds, columns=['ndcg_long', 'ndcg_short'])

        # 对每个交易日计算多空头 ndcg
        for td in tds:
            td_df = df_no_nan[df_no_nan['trading_date'] == td]
            td_ndcg_long, td_ndcg_short = self.__cal_td_ndcg(td_df)
            ndcg_df.loc[td, 'ndcg_long'] = td_ndcg_long
            ndcg_df.loc[td, 'ndcg_short'] = td_ndcg_short

        return ndcg_df

