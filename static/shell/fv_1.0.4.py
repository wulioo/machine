from typing import List

import pandas as pd

from tq_data_client import DBServer

db_server = DBServer()


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


def get_labels(df_with_td_and_wc: pd.DataFrame, return_ods: List[int], sharpe_ods: List[int]):
    """获取收益率标签和夏普比率标签"""

    # 收益周期下限
    return_ods = [od for od in return_ods if od > 0]
    sharpe_ods = [od for od in sharpe_ods if od > 1]

    # 定义标签列
    label_cols = [f'return_{od}' for od in return_ods]
    label_cols += [f'sharpe_{od}' for od in sharpe_ods]

    # 收益周期并集
    for od in sharpe_ods:
        if od not in return_ods:
            return_ods.append(od)

    # 从 future_daily 获取每个日期合约的 close 计算标签
    wcs = df_with_td_and_wc['wind_code'].unique().tolist()
    n = len(wcs)
    wc_dfs = []
    for i, wc in enumerate(wcs):
        print(f'计算标签 {i + 1}/{n} {wc}')
        params = {'fields': 'trading_date,wind_code,close_price', 'wind_code': wc}
        url = f'{db_server.url_root}/tqmain/future_daily'
        wc_df = db_server.get_data(params, url)
        wc_df.sort_values('trading_date', inplace=True, ignore_index=True)
        if len(sharpe_ods) > 0:
            wc_df['pre_close'] = wc_df['close_price'].shift(1)
            wc_df['return'] = wc_df['close_price'] / wc_df['pre_close'] - 1
        for od in return_ods:
            wc_df[f'pro_{od}_close'] = wc_df['close_price'].shift(-od)
            wc_df[f'return_{od}'] = wc_df[f'pro_{od}_close'] / wc_df['close_price'] - 1
            if od in sharpe_ods:
                wc_df[f'return_std_{od}'] = wc_df[f'return'].rolling(od).std(ddof=0)
                wc_df[f'pro_return_std_{od}'] = wc_df[f'return_std_{od}'].shift(-od)
                wc_df[f'sharpe_{od}'] = wc_df.apply(lambda x: 0 if x[f'return_{od}'] == 0
                else x[f'return_{od}'] / x[f'pro_return_std_{od}'],
                                                    axis=1)
        wc_dfs.append(wc_df[['trading_date', 'wind_code'] + label_cols])
    label_df = pd.concat(wc_dfs, ignore_index=True)
    label_df = df_with_td_and_wc.merge(label_df, how='left', on=['trading_date', 'wind_code'])
    return label_df


def get_sharpe(df_with_td_and_wc: pd.DataFrame, sharpe_ods: List[int], use_close: bool = True):
    """仅计算夏普比率标签的代码，收益周期应大于 1"""

    # 定义标签列
    label_cols = [f'sharpe_{od}' for od in sharpe_ods]

    if use_close:
        price = 'close_price'
    else:
        price = 'open_price'

    # 从 future_daily 获取每个日期合约的价格计算标签
    wcs = df_with_td_and_wc['wind_code'].unique().tolist()
    n = len(wcs)
    wc_dfs = []
    params = {'fields': f'trading_date,wind_code,{price}'}
    url = f'{db_server.url_root}/tqmain/future_daily'
    for i, wc in enumerate(wcs):
        print(f'计算标签 {i + 1}/{n} {wc}')
        params['wind_code'] = wc
        wc_df = db_server.get_data(params, url)
        wc_df.sort_values('trading_date', inplace=True, ignore_index=True)  # trading_date 从小到大排列
        if not use_close:  # 使用下一交易日的开盘价
            wc_df[price] = wc_df[price].shift(-1)
        # 计算 1 日收益率（用于计算收益率的波动率）
        wc_df[f'pre_{price}'] = wc_df[price].shift(1)
        wc_df['return'] = wc_df[price] / wc_df[f'pre_{price}'] - 1
        # 对各收益周期计算收益率并除以波动率
        for od in sharpe_ods:
            # 收益率（其实就是第一种标签）
            wc_df[f'pro_{od}_{price}'] = wc_df[price].shift(-od)
            wc_df[f'return_{od}'] = wc_df[f'pro_{od}_{price}'] / wc_df[price] - 1
            # 波动率
            wc_df[f'return_std_{od}'] = wc_df[f'return'].rolling(od).std(ddof=0)
            wc_df[f'pro_return_std_{od}'] = wc_df[f'return_std_{od}'].shift(-od)
            # 收益率除以波动率得到第二种标签
            wc_df[f'sharpe_{od}'] = wc_df.apply(lambda x: 0 if x[f'return_{od}'] == 0
            else x[f'return_{od}'] / x[f'pro_return_std_{od}'],
                                                axis=1)
        wc_dfs.append(wc_df[['trading_date', 'wind_code'] + label_cols])
    label_df = pd.concat(wc_dfs, ignore_index=True)
    label_df = df_with_td_and_wc.merge(label_df, how='left', on=['trading_date', 'wind_code'])
    return label_df


if __name__ == '__main__':
    # 指定品种，起始日期，收益率周期，收益率/波动率周期
    TYPES = ['A.DCE', 'AG.SHF', 'AL.SHF', 'AU.SHF', 'B.DCE', 'BB.DCE', 'BU.SHF', 'C.DCE', 'CS.DCE', 'CU.SHF', 'EB.DCE',
             'EG.DCE', 'FB.DCE', 'FU.SHF', 'HC.SHF', 'I.DCE', 'IC.CFE', 'IF.CFE', 'IH.CFE', 'IM.CFE', 'J.DCE', 'JD.DCE',
             'JM.DCE', 'L.DCE', 'LH.DCE', 'M.DCE', 'NI.SHF', 'P.DCE', 'PB.SHF', 'PG.DCE', 'PP.DCE', 'RB.SHF', 'RR.DCE',
             'RU.SHF', 'SN.SHF', 'SP.SHF', 'SS.SHF', 'T.CFE', 'TF.CFE', 'TS.CFE', 'V.DCE', 'WR.SHF', 'Y.DCE', 'ZN.SHF']
    START, END = '2022-04-25', '2022-10-25'
    RETURN_ODS = [3, 5]
    SHARPE_ODS = [3, 5]

    df = get_dominant_contracts(TYPES, START, END)
    df1 = get_labels(df, RETURN_ODS, SHARPE_ODS)
    df2 = get_sharpe(df, SHARPE_ODS, False)
    df2.sort_values(['wind_code', 'trading_date'])
    pass
