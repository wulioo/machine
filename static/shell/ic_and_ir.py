"""
计算 IC 值和 IR 值
"""

import warnings

import pandas as pd

from tq_data_client import DBServer
warnings.filterwarnings('ignore')

db_server = DBServer()


# 读取数据，取 2018-01-01 之后的数据
df = pd.read_parquet('../../data/fv_data_2018.parq.gz')  # 这里主要是因子数据，有 trading_date 列，标的列，还有许多因子/特征列
df = df[df['trading_date'] >= '2021-01-01']


# 去掉非数值列和原本的标签列，去掉 type_name_ab 空值行
df.drop(columns=['f190', 'f191', 'f192', 'target_1', 'target_2', 'target_3'], inplace=True, errors='ignore')  #删除某些列
df.dropna(subset=['type_name_ab'], inplace=True)  #将列type_name_ab含有nan的删除

# 计算收益率（label_1-4 代表 return_1，3，5，10）
label_ods = [1, 3, 5, 10]
label_cols = [f'label_{i + 1}' for i in range(len(label_ods))]
wcs = df['wind_code'].unique().tolist() #去重 转换成列表
n = len(wcs)
wc_dfs = []
for i, wc in enumerate(wcs):
    print(f'计算标签 {i + 1}/{n} {wc}')
    params = {'fields': 'trading_date,wind_code,close_price', 'wind_code': wc}
    url = f'{db_server.url_root}/tqmain/future_daily'
    wc_df = db_server.get_data(params, url)
    wc_df.sort_values('trading_date', inplace=True, ignore_index=True)
    for iod, od in enumerate(label_ods):
        wc_df[f'pro_{od}_close'] = wc_df['close_price'].shift(-od)
        wc_df[f'label_{iod + 1}'] = (wc_df[f'pro_{od}_close'] / wc_df['close_price'] - 1) * 100
    wc_dfs.append(wc_df[['trading_date', 'wind_code'] + label_cols])
wc_df = pd.concat(wc_dfs, ignore_index=True)
df = df.merge(wc_df, how='left')

# 定义特征、标签、日期
xy = df.columns.tolist()[3:]
xs = xy[:-4]
ys = xy[-4:]
tds = df['trading_date'].unique().tolist()
tds = sorted(tds)

# 计算 Normal IC
corr_dfs = []
for td in tds:
    print(f'计算 normal IC {td}')
    td_df = df[df['trading_date'] == td]
    corr = td_df[xy].corr().loc[ys, xs]
    corr.index.rename('label', inplace=True)
    corr.reset_index(inplace=True)
    corr['trading_date'] = td
    corr_dfs.append(corr)
corr_df = pd.concat(corr_dfs, ignore_index=True)
corr_df.set_index('trading_date', inplace=True)
for y in ys:
    y_corr = corr_df[corr_df['label'] == y]
    y_corr.drop(columns='label', inplace=True)
    y_corr.to_csv(f'normal_IC_{y}.csv')

# 计算 Rank IC
corr_dfs = []
for td in tds:
    print(f'计算 rank IC {td}')
    td_df = df[df['trading_date'] == td]
    corr = td_df[xy].corr(method='spearman').loc[ys, xs]
    corr.index.rename('label', inplace=True)
    corr.reset_index(inplace=True)
    corr['trading_date'] = td
    corr_dfs.append(corr)
corr_df = pd.concat(corr_dfs, ignore_index=True)
corr_df.set_index('trading_date', inplace=True)
for y in ys:
    y_corr = corr_df[corr_df['label'] == y]
    y_corr.drop(columns='label', inplace=True)
    y_corr.to_csv(f'rank_IC_{y}.csv')

# 因子前 20% 的收益率减去后 20%
for y in ys:
    df_no_nan = df.dropna(subset=[y])
    return_df = pd.DataFrame(index=tds, columns=xs)
    for td in tds:
        print(f'计算收益率之差 {y} {td}')
        td_df = df_no_nan[df_no_nan['trading_date'] == td]
        instr_per_group = round(len(td_df) / 5)
        for x in xs:
            x_df = td_df[[x, y]]
            x_df.sort_values(by=x, ascending=False, inplace=True, ignore_index=True)
            return_df.loc[td, x] = x_df[y].iloc[:instr_per_group].mean() - x_df[y].iloc[-instr_per_group:].mean()
    return_df.index.rename('trading_date', inplace=True)
    return_df.to_csv(f'return_{y}.csv')

# 汇总结果
with pd.ExcelWriter('IC_summary.xlsx') as writer:
    for y in ys:
        y_df = pd.DataFrame(index=xs)
        ret = pd.read_csv(f'return_{y}.csv', index_col='trading_date')
        corr_pearson = pd.read_csv(f'normal_IC_{y}.csv', index_col='trading_date')
        corr_spearman = pd.read_csv(f'rank_IC_{y}.csv', index_col='trading_date')
        y_df['return_mean'] = ret.mean()
        y_df['normal_IC_mean'] = corr_pearson.mean()
        y_df['normal_IC_std'] = corr_pearson.std(ddof=0)
        y_df['normal_IC>0.02'] = (corr_pearson > 0.02).sum() / corr_pearson.count()
        y_df['normal_IC<-0.02'] = (corr_pearson < -0.02).sum() / corr_pearson.count()
        y_df['normal_IR'] = y_df['normal_IC_mean'] / y_df['normal_IC_std']
        y_df['rank_IC_mean'] = corr_spearman.mean()
        y_df['rank_IC_std'] = corr_spearman.std(ddof=0)
        y_df['rank_IC>0.02'] = (corr_spearman > 0.02).sum() / corr_spearman.count()
        y_df['rank_IC<-0.02'] = (corr_spearman < -0.02).sum() / corr_spearman.count()
        y_df['rank_IR'] = y_df['rank_IC_mean'] / y_df['rank_IC_std']
        y_df.index.rename('factor', inplace=True)
        y_df.to_excel(writer, sheet_name=y)

print('完毕。')
