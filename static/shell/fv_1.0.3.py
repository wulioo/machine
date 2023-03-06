from typing import List, Dict

import pandas as pd
from loguru import logger

from tq_data_client import DBServer

db_server = DBServer()

"""
在查询 fv_factor_info 表，当遇到 table_name 和 factor_name 一样，
也就是以下 4 个因子的时候，因为表结构和其他因子表不同，需要做一些特殊处理。

section = [
    'standardized_basis',
    'momentum',
    'inventory',
    'basis',
]

这些因子是一个因子一张表，因子列的列名是 'factor' 而不是因子名，且品种列是 type_name，不是 type_name。

所以需要做以下两个处理：
1. 列名 factor 改成 table_name，列名 type_name 改成 type_name_ab
2. type_name 列中的值转成 type_name_ab
"""


# 从 future_header 提取不重复的 type_name_ab，然后将 type_name_ab 点号前面的部分小写转成 type_name，
# 从而制作一个 type_name 和 type_name_ab 的映射字典
def get_type_dict() -> Dict[str, str]:
    """获取 type_name 与 type_name_ab 的对应字典"""
    type_dict = {}
    params = {'fields': 'type_name_ab'}
    url = f'{db_server.url_root}/tqmain/future_header'
    type_df = db_server.get_data(params=params, url=url)
    if type_df.empty:
        logger.error('future_header empty')
    else:
        type_df.drop_duplicates(inplace=True)
        type_df['type_name'] = type_df['type_name_ab'].str.extract('([A-Z]+)\\.')
        type_df['type_name'] = type_df['type_name'].str.lower()
        type_dict = dict(zip(type_df['type_name'], type_df['type_name_ab']))
    return type_dict


table_name = 'basis'
df = ...  # 比如说，提取出来 basis 这张因子表

if 'type_name' in df.columns:
    # 列名 factor 改成 table_name，列名 type_name 改成 type_name_ab
    df.rename(columns={'type_name': 'type_name_ab', 'factor': table_name}, inplace=True)
    # 获取 type_name 与 type_name_ab 的对应字典
    type_dict = get_type_dict()
    # type_name 列中的值转成 type_name_ab，并检查所有 type_name 都被转换成 type_name_ab
    df['type_name_ab'] = df['type_name_ab'].replace(type_dict)
    assert df['type_name_ab'].str.contains('\\.').all(), 'not all type_name transferred to type_name_ab'


"""
一个表涉及到的品种，用之前的方法对 type_name_ab 去重得到就行，这里还要去掉金融期货品种:
['IC.CFE', 'IF.CFE', 'IH.CFE', 'IM.CFE', 'T.CFE', 'TF.CFE', 'TS.CFE']。
多个表涉及到的品种，取并集。
已经上市的品种，因为因子计算窗口期某天没有因子数值，也要填充中位数和均值，这里和原来的方法有些不一样的处理。
"""


def get_dominant_contracts(types: List[str], start: str, end: str):
    """指定品种列表和起止日期获取主力合约，用于计算标签"""
    n = len(types)
    t_dfs = []
    for i, t in enumerate(types):
        print(f'获取主力合约 {i + 1}/{n} {t}')
        params = {'type_name_ab': t}
        url = f'{db_server.url_root}/tqmain/future_dominant_daily'
        t_df = db_server.get_data(params, url)
        if not t_df.empty:
            t_df = t_df[t_df['trading_date'] >= start]
            t_df = t_df[t_df['trading_date'] <= end]
            t_dfs.append(t_df[['trading_date', 'type_name_ab', 'wind_code']])
    dominant_df = pd.concat(t_dfs, ignore_index=True)
    dominant_df.sort_values(['trading_date', 'type_name_ab'], inplace=True, ignore_index=True)
    return dominant_df


# 用户指定起止日期
start_date = '2011-01-01'
end_date = '2022-09-30'

df = ...  # 根据用户指定起止日期获取因子数据
# 剔除金融期货
df = df[~df['type_name_ab'].isin(['IC.CFE', 'IF.CFE', 'IH.CFE', 'IM.CFE', 'T.CFE', 'TF.CFE', 'TS.CFE'])]

# 根据【整个因子表涉及的品种】和【用户指定的起止日期】获取 dominant 表（之前是根据已提取的 df 中涉及的 type）
future_types = ...  # 这里不要用 df['type_name_ab'].unique().tolist()，而要用整个因子表涉及的品种，除了金融期货品种
df_dominant = get_dominant_contracts(future_types, start_date, end_date)

# 使用 dominant 去除品种上市前的特征数据，已上市但无因子数据的也可以包括进来
df_feature = df_dominant.merge(df, how='left', on=['trading_date', 'type_name_ab'])

# 之后根据 wc 计算收益率就行，和之前一样


"""
因子数据各日期截面用中位数/均值填充空值
"""


def fill_td_median(df: pd.DataFrame, cols: List[str]):
    """各日期截面用中位数填充空值"""
    tds = df['trading_date'].unique().tolist()
    td_dfs = []
    for td in tds:
        td_df = df[df['trading_date'] == td]
        td_df[cols] = td_df[cols].fillna(td_df[cols].quantile())
        td_dfs.append(td_df)
    df_filled = pd.concat(td_dfs)
    return df_filled


def fill_td_mean(df: pd.DataFrame, cols: List[str]):
    """各日期截面用均值填充空值"""
    tds = df['trading_date'].unique().tolist()
    td_dfs = []
    for td in tds:
        td_df = df[df['trading_date'] == td]
        td_df[cols] = td_df[cols].fillna(td_df[cols].mean())
        td_dfs.append(td_df)
    df_filled = pd.concat(td_dfs)
    return df_filled
