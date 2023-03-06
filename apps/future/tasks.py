import datetime
import json
import os
import pickle
import time
import uuid

import pandas as pd
import pymysql
from celery import shared_task
from django.core.cache import cache
from matplotlib import pyplot as plt

from Machine.settings import STATICFILES_DIRS, BASE_DIR
from logs import logger
from service.ndcg import Ndcg
from utils.common import TimeContext


@shared_task
def celery_ic(tds, uuid_df):
    df = cache.get(uuid_df)['df']
    factor = cache.get(uuid_df)['factor']
    corr_dfs = factor.cal_single_rank_normal_ic(df, tds)

    return corr_dfs


@shared_task
def celery_earnings(wc_list, label_ods, parma_id):
    parma = cache.get(parma_id)
    price_df = parma['price_df']
    ear = parma['ear']
    result = ear.single_earnings(wc_list, price_df, label_ods)
    return pd.concat(result, ignore_index=True).to_json()


@shared_task
def celery_ndcg(df, fl):
    df = pd.read_json(df, encoding="utf-8", orient='records')

    result = {}
    for label, factor in fl:
        with TimeContext(f'计算NDCG-{factor}-{label} cpu'):
            if not result.get(label):
                result[label] = []
            df_no_nan = df.dropna(subset=[factor, label])
            tds = sorted(df_no_nan['trading_date'].unique().tolist())
            ndcg = Ndcg(5, factor, label)
            ndcg_df = ndcg.celery_ndcg(df_no_nan, tds)
            ndcg_df_mean = pd.DataFrame({'avg_ndcg_long': ndcg_df['ndcg_long'].mean(), 'avg_ndcg_short': ndcg_df['ndcg_short'].mean()}, index=[factor]).to_json()
            result[label].append(ndcg_df_mean)
    return result


@shared_task
def celery_layered(f, uuid_df):
    df = cache.get(uuid_df)['df']
    factor = cache.get(uuid_df)['factor']
    return factor.single_group_cumsum(df,f)

@shared_task
def celery_factor_diff(uuid_df, tds, y):
    df = cache.get(uuid_df)['df']
    factor = cache.get(uuid_df)['factor']
    result = factor.cal_single_return_mean(df, tds, y)
    return result.to_json()


@shared_task
def celery_factor_eq_diff(uuid_df, tds, y, xs, factor_diff):
    """
    计算股票 因子前后差异
    :param uuid_df:
    :param tds:
    :param y:
    :param xs:
    :param factor_diff:
    :return:
    """
    df = cache.get(uuid_df)

    # 多空
    return_df = pd.DataFrame(index=tds, columns=xs)
    # 多头
    long_df = pd.DataFrame(index=tds, columns=xs)
    # 空头
    short_df = pd.DataFrame(index=tds, columns=xs)
    for td in tds:
        td_df = df[df['trading_date'] == td]
        for x in xs:
            x_df = td_df[[x, y]]
            x_df.dropna(subset=[x, y], inplace=True)
            instr_per_group = round(len(x_df) / 5)
            if instr_per_group == 0:
                continue
            x_df.sort_values(by=x, ascending=False, inplace=True, ignore_index=True)
            for diff in factor_diff:
                if diff == 'ls_return_mean':
                    return_df.loc[td, x] = x_df[y].iloc[:instr_per_group].mean() \
                                           - x_df[y].iloc[-instr_per_group:].mean()
                elif diff == 'lo_return_mean':
                    long_df.loc[td, x] = x_df[y].iloc[:instr_per_group].mean() - x_df[y].mean()

                elif diff == 'so_return_mean':
                    short_df.loc[td, x] = x_df[y].mean() - x_df[y].iloc[-instr_per_group:].mean()

    return_df.index.rename('trading_date', inplace=True)
    long_df.index.rename('trading_date', inplace=True)
    short_df.index.rename('trading_date', inplace=True)
    data = {}
    for diff in factor_diff:
        if diff == 'ls_return_mean':
            data[diff] = return_df.to_json()
        elif diff == 'lo_return_mean':
            data[diff] = long_df.to_json()
        elif diff == 'so_return_mean':
            data[diff] = short_df.to_json()
    return data


@shared_task
def celery_box_muster_chart(factor_column, factor_list, type_name):
    factor_column = pd.read_json(factor_column, encoding="utf-8", orient='records')
    f_list = {}
    for x in factor_list:
        with TimeContext(f'{x}-画盒须图 io'):
            x_df = factor_column[['trading_date', type_name, x]]
            x_df.dropna(subset=x, inplace=True)
            x_df1 = x_df.pivot(index='trading_date', columns=type_name).reset_index(drop=True)
            x_df1.columns = [i[1] for i in x_df1.columns]
            x_df1.boxplot(figsize=(24, 8), grid=False, showmeans=True, rot=30)
            plt.title(f'{x} distribution per type', size=15)

            plt.grid(True, alpha=.5, ls='--')
            key_uuid = uuid.uuid1()
            file_name = os.path.join(STATICFILES_DIRS[0], f'images/{key_uuid}.png')
            plt.savefig(file_name, bbox_inches='tight')
            plt.close()
        f_list[x] = f'static/images/{key_uuid}.png'
    return f_list


@shared_task
def celery_backtesting(wc_and_erg, factor_group_label, num):
    wc_and_erg = pd.read_json(wc_and_erg, encoding="utf-8", orient='records')
    result = {}
    for factor, holding_od in factor_group_label:
        label_col = f'label_{holding_od}'
        if not result.get(factor):
            result[factor] = {}

        with TimeContext(f'计算单因子-{factor}-{num}-{holding_od} cpu'):
            wc_and_erg['trading_date'] = pd.to_datetime(wc_and_erg['trading_date'], unit='s')

            # 1.drop 掉收益率为空的行
            df_no_nan = wc_and_erg.dropna(subset=[label_col, factor])
            # 初始化以交易日为 index，各层为 columns 的 df
            tds = df_no_nan['trading_date'].astype(str).unique().tolist()
            tds = sorted(tds)
            group_return = pd.DataFrame(index=tds, columns=[f'group{i + 1}' for i in range(num)])
            group_return.index.rename('trading_date', inplace=True)

            for td in tds:
                td_df = df_no_nan[df_no_nan['trading_date'] == td]
                td_df.sort_values(by=[factor, 'wind_code'], ascending=[False, True], inplace=True, ignore_index=True)
                avg_ret = td_df[label_col].mean()
                instr_per_group = len(td_df) / num

                for i in range(num):
                    group_avg_ret = td_df[label_col].iloc[
                                    round(i * instr_per_group):round((i + 1) * instr_per_group)].mean()
                    group_return.loc[td, f'group{i + 1}'] = group_avg_ret - avg_ret

            # 按持有天数间隔交易日
            tds = group_return.index.tolist()[::holding_od]
            group_return = group_return.loc[tds]

            # 各层超额收益率累加后 +1
            for i in range(num):
                group_return[f'group{i + 1}'] = (group_return[f'group{i + 1}']).cumsum() + 1

        result[factor][label_col] = ((group_return['group1'] - group_return['group5']) / 2).to_json()
    return result
