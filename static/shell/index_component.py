"""
根据指数筛选股票

# 指数名称与代码的对应，名称可以显示在前端，代码用于查询数据
INDEX_CODES = {
    '沪深300': '000300.SH',
    '上证50': '000016.SH',
    '中证500': '000905.SH',
    '中证1000': '000852.SH',
    # '创业板指': '399006.SZ',
    # '国证2000': '399303.SZ',
}
"""

from typing import List

import pymysql
import pandas as pd


# 连接 MySQL 准备，使用自己的用户名和密码
CONFIG = {
    'host': '192.168.1.160',
    'port': 3306,
    'user': 'daihuizheng',
    'passwd': 'Iry7X+pP7D0E+A==',
}


def get_mysql_data(sql_query: str) -> pd.DataFrame:
    """使用 sql 语句从 mysql 中获取数据，返回 df"""
    conn = pymysql.connect(**CONFIG)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    df = pd.DataFrame(result)
    if not df.empty:
        col = cursor.description
        columns = [i[0] for i in col]
        df.columns = columns
    conn.close()
    return df


def get_index_component(trading_date: str, index_code: str) -> List[str]:
    """使用 sql 语句从 mysql 中获取数据，返回 df"""
    conn = pymysql.connect(**CONFIG)
    cursor = conn.cursor()
    sql_query = f'''
        select wind_code from tqmain.index_component
        where trading_date = '{trading_date}'
        and index_code = '{index_code}'
    '''
    cursor.execute(sql_query)
    result = cursor.fetchall()
    conn.close()
    index_component = []
    if result:
        index_component = [i[0] for i in result]
    return index_component


if __name__ == '__main__':

    '''从前台获取的参数'''
    td = '2022-09-29'  # 交易日，因为指数成分股会根据日期变化，所以只能一天一天地取
    index_code = '000852.SH'  # 指数代码
    table_name = 'eq_1d_volprice_1'  # 表名
    xs = ['jor', 'alpha10']  # 因子列表
    xs_string = ', '.join(xs)

    '''根据指数获取 wind_code 列表，可用于分批计算收益率'''
    wc_list = get_index_component(td, index_code)

    '''根据指数提取因子表数据'''
    sql = f'''
        select trading_date, wind_code, {xs_string} from tq_factor.{table_name}
        where trading_date = '{td}'
        and wind_code in (
            select wind_code from tqmain.index_component
            where trading_date = '{td}'
            and index_code = '{index_code}'
        );
    '''
    factor_df = get_mysql_data(sql)
