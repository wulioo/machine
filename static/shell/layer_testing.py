"""
分层测试

输出文件名中：
group_return_5_predict_1_return_5 代表分 5 层，预测值为 predict_1，持有天数是 5 天（对应未来 5 日收益率）
group_return_5_1_predict_1_return_5 代表分 5 层，其中第 1 层不同开始日期的对比，预测值为 predict_1，持有天数是 5 天（对应未来 5 日收益率）
"""

import warnings
from typing import List

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

from tq_data_client import DBServer

warnings.filterwarnings('ignore')
db_server = DBServer(usr='daihuizheng', pwd='Iry7X+pP7D0E+A==')  # 这里请使用自己的用户名和密码，如果遇到权限问题，可以发邮件给周扬


# 创建 layer_testing 文件夹
LAYER_TESTING_PATH = './layer_testing/'
p = Path(LAYER_TESTING_PATH)
if not p.exists():
    p.mkdir()


def get_returns(df_with_td_and_type: pd.DataFrame, return_ods: List[int]):
    """获取未来指定天数的收益率，不乘以 100"""
    return_cols = [f'return_{od}' for od in return_ods]

    # 从 future_dominant_daily 获取日期品种的主力合约
    types = df_with_td_and_type['type_name_ab'].unique().tolist()
    n = len(types)
    t_dfs = []
    for i, t in enumerate(types):
        print(f'获取主力合约 {i + 1}/{n} {t}')
        params = {'type_name_ab': t}
        url = f'{db_server.url_root}/tq_model/future_dominant_daily'
        t_df = db_server.get_data(params, url)
        t_dfs.append(t_df[['trading_date', 'type_name_ab', 'wind_code']])
    t_df = pd.concat(t_dfs, ignore_index=True)
    df_with_td_and_wc = df_with_td_and_type.merge(t_df, how='left')

    # 从 future_daily 获取日期合约的收盘价并计算收益率
    wcs = df_with_td_and_wc['wind_code'].unique().tolist()
    n = len(wcs)
    wc_dfs = []

    for i, wc in enumerate(wcs):
        print(f'计算标签 {i + 1}/{n} {wc}')
        params = {'fields': 'trading_date,wind_code,close_price', 'wind_code': wc}
        url = f'{db_server.url_root}/tqmain/future_daily'
        wc_df = db_server.get_data(params, url)
        wc_df.sort_values('trading_date', inplace=True, ignore_index=True)
        for od in return_ods:
            wc_df[f'pro_{od}_close'] = wc_df['close_price'].shift(-od)
            wc_df[f'return_{od}'] = wc_df[f'pro_{od}_close'] / wc_df['close_price'] - 1
        wc_dfs.append(wc_df[['trading_date', 'wind_code'] + return_cols])
    wc_df = pd.concat(wc_dfs, ignore_index=True)
    df_with_return = df_with_td_and_wc.merge(wc_df, how='left')
    df_with_return.drop(columns='wind_code', inplace=True)

    return df_with_return


def get_group_return(n_group, df_with_predict_and_return, predict_col, holding_period):
    """指定层数、预测值、持有天数，计算每个交易日各层的超额收益率"""

    # 如果已经计算过了就跳过
    group_return_file = LAYER_TESTING_PATH + f'group_return_{n_group}_{predict_col}_return_{holding_period}.csv'
    if Path(group_return_file).exists():
        return

    # drop 掉收益率为空的行
    return_col = f'return_{holding_period}'
    df_no_nan = df_with_predict_and_return.dropna(subset=[return_col])

    # 初始化以交易日为 index，各层为 columns 的 df
    tds = df_no_nan['trading_date'].unique().tolist()
    tds = sorted(tds)
    group_return = pd.DataFrame(index=tds, columns=[f'group{i+1}' for i in range(n_group)])
    group_return.index.rename('trading_date', inplace=True)

    # 每个交易日内所有品种按预测值排序分层，每一层的收益率均值减去所有品种的均值为这一层的超额收益率
    for td in tds:
        td_df = df_no_nan[df_no_nan['trading_date'] == td]
        td_df.sort_values(by=predict_col, ascending=False, inplace=True, ignore_index=True)
        avg_ret = td_df[return_col].mean()
        instr_per_group = len(td_df) // n_group
        for i in range(n_group):
            group_avg_ret = td_df[return_col].iloc[i*instr_per_group:(i+1)*instr_per_group].mean()
            group_return.loc[td, f'group{i+1}'] = group_avg_ret - avg_ret

    # 保存计算结果
    group_return.to_csv(group_return_file)
    return


def draw_group_cumsum(n_group, predict_col, holding_period, start=None, end=None):
    """分层测试绘图"""

    # 读取对应层数、预测值、持有天数的分层数据
    group_return_file = LAYER_TESTING_PATH + f'group_return_{n_group}_{predict_col}_return_{holding_period}.csv'
    group_return = pd.read_csv(group_return_file, index_col='trading_date')

    # 指定起止日期
    if start is not None:
        group_return = group_return[group_return.index >= start]
    if end is not None:
        group_return = group_return[group_return.index <= end]

    # 按持有天数间隔交易日
    tds = group_return.index.tolist()[::holding_period]
    group_return = group_return.loc[tds]

    # 各层超额收益率累加后 +1
    for i in range(n_group):
        group_return[f'group{i+1}'] = (group_return[f'group{i+1}']).cumsum() + 1

        # 保存计算结果
    group_return.to_csv(group_return_file)
    # 绘图
    # group_return.index = pd.to_datetime(group_return.index)
    # group_return.plot(figsize=(20, 5))
    # plt.hlines(1, group_return.index.min(), group_return.index.max(), alpha=0.5)
    # plt.grid(axis='y', alpha=0.5, ls='--')
    # plt.savefig(LAYER_TESTING_PATH + f'group_return_{n_group}_{predict_col}_return_{holding_period}.png')
    # plt.close()


def draw_start_compare(n_group, predict_col, holding_period, start=None, end=None):
    """对比不同开始日期同一层"""

    # 读取对应层数、预测值、持有天数的分层数据
    group_return_file = LAYER_TESTING_PATH + f'group_return_{n_group}_{predict_col}_return_{holding_period}.csv'
    group_return = pd.read_csv(group_return_file, index_col='trading_date')

    # 指定起止日期
    if start is not None:
        group_return = group_return[group_return.index >= start]
    if end is not None:
        group_return = group_return[group_return.index <= end]

    # 对每一层，根据持有天数指定不同开始日期，分别间隔交易日后累加超额收益率再 +1，绘出不同开始日期之间的对比
    tds = group_return.index.tolist()
    group_return.index = pd.to_datetime(group_return.index)
    for i in range(n_group):
        group = f'group{i+1}'
        plt.figure(figsize=(20, 5))
        for j in range(holding_period):
            j_tds = tds[j::holding_period]
            series = group_return.loc[j_tds, group].cumsum() + 1
            plt.plot(series.index, series.values, label=j_tds[0])
        plt.hlines(1, group_return.index.min(), group_return.index.max(), alpha=0.5)
        plt.grid(axis='y', alpha=0.5, ls='--')
        plt.legend()
        plt.savefig(LAYER_TESTING_PATH + f'group_return_{n_group}_{i+1}_{predict_col}_return_{holding_period}.png')
        plt.close()


if __name__ == '__main__':

    # from util import LABEL_NUM
    LABEL_NUM = 2
    # 指定持有天数
    holding_ods = [5, 10]

    # 读取标签预测值，从 DBServer 获取收益率（与持有天数对应），合并二者并保存
    if not Path('../../data/dnn_predict_mean_with_return.csv').exists():
        df = pd.read_csv('../../data/dnn_predict_mean.csv')
        df = get_returns(df, holding_ods)
        df.to_csv('../../data/dnn_predict_mean_with_return.csv', index=False)
    else:
        df = pd.read_csv('../../data/dnn_predict_mean_with_return.csv')

    # 计算分层数据并绘图
    print('每种预测值分别与每种持有天数组合，计算分层数据并绘图')
    for predict in [f'predict_{i+1}' for i in range(LABEL_NUM)]:
        for holding_od in holding_ods:
            print(f'预测值：{predict}，持有天数：{holding_od}')
            get_group_return(5, df, predict, holding_od)
            draw_group_cumsum(5, predict, holding_od)

    print('预测值和持有天数匹配，对比同一层不同开始日期的走势')
    predict_holding_dict = {
        'predict_1': 5,
        'predict_2': 10,
    }

    for predict, holding_od in predict_holding_dict.items():
        print(f'预测值：{predict}，持有天数：{holding_od}')
        if holding_od > 1:
            get_group_return(5, df, predict, holding_od)
            draw_start_compare(5, predict, holding_od)
