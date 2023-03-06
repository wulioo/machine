"""
计算排序评估指标 NDCG，每个交易日多头和空头各计算一个，然后按指定的起止日期平均起来
"""
import time

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def cal_td_ndcg(n_group: int, td_df: pd.DataFrame, factor_col: str, label_col: str) -> (float, float):
    """计算一个交易日的多空头 ndcg"""

    # 计算当天每层 instrument 个数，多空头收益率减去最小值转为非负数
    instr_per_group = len(td_df) / n_group
    td_df[f'{label_col}_long'] = td_df[label_col] - td_df[label_col].min()
    td_df[f'{label_col}_short'] = - td_df[label_col] - (-td_df[label_col]).min()

    # 多头、空头收益率按因子值降序、自降序排列
    label_long = td_df.sort_values(by=factor_col, ascending=False, ignore_index=True)[f'{label_col}_long']
    label_long_ideal = td_df[f'{label_col}_long'].sort_values(ascending=False, ignore_index=True)
    label_short = td_df.sort_values(by=factor_col, ascending=False, ignore_index=True)[f'{label_col}_short']
    label_short_ideal = td_df[f'{label_col}_short'].sort_values(ascending=False, ignore_index=True)

    # 计算各层折损和平均收益率
    group_df = pd.DataFrame(columns=['discount', 'long', 'long_ideal', 'short', 'short_ideal'])
    for i in range(n_group):
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


def cal_avg_ndcg(n_group: int, df: pd.DataFrame, factor_col: str, label_col: str, start=None, end=None) -> (float, float):
    """指定层数、因子、标签、起止日期，计算日均多空头 ndcg"""

    # # 指定起止日期
    # if start is not None:
    #     df = df[df['trading_date'] >= start]
    # if end is not None:
    #     df = df[df['trading_date'] <= end]

    # drop 掉因子或标签为空的行
    df_no_nan = df.dropna(subset=[factor_col, label_col])

    # 初始化以 trading_date 为 index 的 ndcg_df
    tds = df_no_nan['trading_date'].unique().tolist()
    tds = sorted(tds)
    ndcg_df = pd.DataFrame(index=tds, columns=['ndcg_long', 'ndcg_short'])

    # 对每个交易日计算多空头 ndcg
    for td in tds:
        td_df = df_no_nan[df_no_nan['trading_date'] == td]
        td_ndcg_long, td_ndcg_short = cal_td_ndcg(n_group, td_df, factor_col, label_col)
        ndcg_df.loc[td, 'ndcg_long'] = td_ndcg_long
        ndcg_df.loc[td, 'ndcg_short'] = td_ndcg_short

    # 计算日均 ndcg
    avg_ndcg_long = ndcg_df['ndcg_long'].mean()
    avg_ndcg_short = ndcg_df['ndcg_short'].mean()
    return avg_ndcg_long, avg_ndcg_short


if __name__ == '__main__':

    df = pd.read_csv('dnn_predict_mean_with_return.csv')
    factors = ['predict_1', 'predict_2']
    labels = ['return_5', 'return_10']
    start_date = '2020-01-01'
    end_date = '2021-12-31'
    stime = time.time()
    for factor in factors:
        for label in labels:
            ndcg_long, ndcg_short = cal_avg_ndcg(5, df, factor, label, start_date, end_date)
            print(f'factor: {factor}, label: {label}, {start_date} ~ {end_date} '
                  f'多头 NDCG: {round(ndcg_long, 4)}, 空头 NDCG: {round(ndcg_short, 4)}')

    print(time.time() - stime)
