import pandas as pd

"""
校验IC是否一致 脚本
"""

csv_dict = {
    'normal_IC_return_1': 'pearson_IC_label_1',
    'normal_IC_return_3': 'pearson_IC_label_2',
    'normal_IC_return_5': 'pearson_IC_label_3',
    'normal_IC_return_10': 'pearson_IC_label_4',
    'rank_IC_return_1': 'spearman_IC_label_1',
    'rank_IC_return_3': 'spearman_IC_label_2',
    'rank_IC_return_5': 'spearman_IC_label_3',
    'rank_IC_return_10': 'spearman_IC_label_4',
    'IC_summary': 'summary_IC'

}
for yt_csv, zdh_csv in csv_dict.items():
    if yt_csv == "IC_summary":
        """比对最终结果"""
        yt_df = pd.read_excel(f'../ic_and_ir/{yt_csv}.xlsx', sheet_name='return_1')
        zdh_df = pd.read_excel(f'../ic_and_ir/{zdh_csv}.xlsx', sheet_name='label_1')
        yt_df.set_index('factor', inplace=True)
        zdh_df.set_index('factor', inplace=True)
        check_df = yt_df.merge(zdh_df, how="outer", on='factor')
        # 绝对值
        columns_list = yt_df.columns.tolist()
    else:
        yt_df = pd.read_csv(f'../ic_and_ir/{yt_csv}.csv')
        zdh_df = pd.read_csv(f'../ic_and_ir/{zdh_csv}.csv')
        zdh_df['trading_date'] = pd.to_datetime(zdh_df['trading_date'], format="%Y-%m-%d")
        yt_df['trading_date'] = pd.to_datetime(yt_df['trading_date'], format="%Y-%m-%d")
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

        print(f'{yt_csv}-{factor_col}: ic一致')

    # 相对值
    # diff_result = (check_df['inventory1_x'] - check_df['inventory1_y']) / check_df['inventory1_x']
    # diff_result = diff_result.describe()
