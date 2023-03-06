"""
分层测试校准 脚本
"""
import warnings

import pandas as pd
import pymysql as pymysql

warnings.filterwarnings('ignore')

db = pymysql.connect(host='192.168.1.160',
                     user='daihuizheng',
                     password='Iry7X+pP7D0E+A==',
                     database='tq_factor',
                     charset='utf8',
                     )
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT * from fv_1d_ai_1 limit 1")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()
fileds = [filed[0] for filed in cursor.description]
fileds = [filed for filed in fileds if filed not in ['trading_date', 'type_name_ab', 'upload_user', 'upload_time']]
fileds = {f'group_return_5_{filed}': f'zdh-{filed}' for filed in fileds}
# print(fileds)
# 关闭数据库连接
db.close()

for yt_csv, zdh_csv in fileds.items():
    for index, erg in enumerate([1, 3, 5, 10]):
        yt_df = pd.read_csv(f'../layer_testing/{yt_csv}_return_{erg}.csv')
        zdh_df = pd.read_csv(f'../layer_testing/{zdh_csv}-label_{index + 1}.csv')
        check_df = yt_df.merge(zdh_df, how="outer", on='trading_date')
        # 绝对值
        columns_list = yt_df.drop(columns='trading_date').columns.tolist()
        for factor_col in columns_list:

            diff_result = check_df[f'{factor_col}_x'].describe() - check_df[f'{factor_col}_y'].describe()
            is_nan = check_df[f'{factor_col}_x'].isna().sum() == check_df[f'{factor_col}_y'].isna().sum()
            if not is_nan:
                print(f'{yt_csv}-{factor_col}:空值不一致')
                exit(1)

            if (diff_result.abs() >= 1e-6).any():
                print(f'{yt_csv}-{factor_col}:绝对值大于 1e6')
                exit(1)

            print(f'{yt_csv}-{factor_col}: 分层数据一致一致')
