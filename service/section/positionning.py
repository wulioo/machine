import pandas as pd
from django.db.models import Q

from extra.db.models_tqmain import FutureDominantDaily, FutureHeader, FutureDaily
from service.facotr_base import FvAnalysisBase
from service.factor import FutureFactor
from service.layered import LayeredPosition
from service.night import NightTrading
from service.periods import PositioningPeriods
from utils.common import Common


class FactorPositioning:
    __weight: int
    periods: PositioningPeriods
    layered: LayeredPosition

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight):
        self.__weight = weight

    def _get_factor(self):
        """
         1）由N个因子，确定计算持仓要用到哪些因子；
         2）由输入日期（e.g.2022-12-02），选定基准日；
         3）由收益周期（e.g.1或5），选定拉去1天（20221202）or5天（20221128-20221202）的因子数据；
         对每个因子的、每一天的数据做排序，
         """
        return self.periods.get_factor(self)

    def _filter_type_name_ab(self, df, type_name_ab):
        factor_df = df[~df['type_name_ab'].isin(type_name_ab)]
        factor_df.reset_index(inplace=True)
        factor_df.drop(['index'], axis=1, inplace=True)
        return factor_df

    def _get_long_short(self, df: pd.DataFrame):
        """
        4）由分层层数（e.g.5层），得到每层平均有几个type-name-ab，记作M = 总数/层数；（暂定四舍五入）
        5）选定排序最前M个为多头持仓，最后M个为空头持仓；
        """
        long, short = self.layered.cur_date_layered(df)
        return long, short

    def _cal_theory_position(self, df: pd.DataFrame):
        """
        6）由收益周期确定每天的权重，如1天则权重为1/1=100%，如5天则每天权重为1/5=20%；
        --------------------------------
        假如5天收益周期 假如标的 有两种【AL.SHF, TA.CAZ】, AL.SHF有3个，哪就是 3/5=60% （这个是叫权重是吗？）
        TA.CAZ有1个，1/5 = 20% （AL.SHF权重为60%，TA.CAZ权重为20%）

        7）从5）中选出来的标的，对应权重为6）的每天权重 * 因子权重（用户输入）；理论持仓
        --------------------------------
        因子权重是前端传过来的数据 用户输入的，每天的权重 就是每个标的的权重
        """
        df_type = pd.DataFrame(df.type_name_ab.value_counts())
        df_type['theory_position'] = (df_type / self.periods.label) * self.__weight
        df_type.reset_index(inplace=True)
        df_type.rename(columns={'index': 'type_name_ab', 'type_name_ab': 'count', self.column: 'section'}, inplace=True)
        return df_type

    def _get_main_contracts(self, df: pd.DataFrame):
        """
         8）从type-name-ab拿到当日的主力合约；
        """
        main_contracts = FutureDominantDaily.get_info_all(Q(type_name_ab__in=df['type_name_ab']) & Q(trading_date=self.stime), ['trading_date', 'type_name_ab', 'wind_code'],
                                                          'tqmain')
        df_type = df.merge(main_contracts, how='left', on=['type_name_ab'])
        return df_type

    def _cal_money_mean(self, df: pd.DataFrame):
        """
        9）由交易金额和4）中的M，得到标的平均交易金额；
        -------------------------------------
        交易金额（前端用户手动输入）
        4）中的M = type-name-ab总数/层数，即每层平均有几个type-name-ab
        平均交易金额 = 交易金额/M/收益周期
        """
        df['mean_money'] = self.layered.money / df['count'].sum() * df['count']
        # df['mean_money'] = self.layered.money_mean / self.periods.label
        return df

    def _cal_actual_position(self, df: pd.DataFrame):
        """
        10）由8）中合约的价格，乘数，和9）中的标的平均交易金额，得到实际持仓。（四舍五入）
        -------------------------------------
        乘数，future_header的contract_multiplier字段
        价格，future_daily表的 close_price
        平均交易金额，是9）计算的到的结果
        最后的实际持仓 = 平均交易金额 / 价格 / 乘数 ，再四舍五入 （取整）
        """
        contract_multiplier = FutureHeader.get_info_all(Q(wind_code__in=df['wind_code']), ['wind_code', 'contract_multiplier'], 'tqmain')
        close_price = FutureDaily.get_info_all(Q(wind_code__in=df['wind_code']) & Q(trading_date=self.stime), ['trading_date', 'close_price', 'wind_code'], 'tqmain')
        df_type = df.merge(contract_multiplier, how='left', on=['wind_code'])
        df_type = df_type.merge(close_price, how='left', on=['wind_code', 'trading_date'])
        df_type['actual_position'] = (df_type['mean_money'] / df_type['close_price'] / df_type['contract_multiplier']) * df_type['long_short'].replace(['+', "-"], [1, -1])
        return df_type

    def _cal_sum_money(self, df: pd.DataFrame):
        df['position_money'] = round(df['actual_position'] * df['contract_multiplier'] * df['close_price'])
        df['p_moeny_sum'] = df['position_money'].sum()
        return df

    def cal_positioning(self, type_name_ab):
        factor_df = self._get_factor()

        factor_df = self._filter_type_name_ab(factor_df, type_name_ab)

        long, short = self._get_long_short(factor_df)
        result = dict()
        for name, df in {'+': long, '-': short}.items():
            position_df = self._cal_theory_position(df)
            position_df['long_short'] = name
            position_df = self._get_main_contracts(position_df)
            position_df = self._cal_money_mean(position_df)

            position_df = self._cal_actual_position(position_df)
            position_df = self._cal_sum_money(position_df)

            # result = pd.concat([result, position_df], ignore_index=True)
            position_df.loc[:, 'trading_date'] = Common.get_next_trading_time(position_df['trading_date'].iloc[0])
            position_df['trading_date'] = position_df['trading_date'].astype(str)

            result[name] = position_df
        return result

    def many_factor_merge(self, positioning):
        new_arr = []
        merge_field = ['trading_date', 'wind_code', 'type_name_ab', 'close_price', 'contract_multiplier']

        if len(positioning) > 1:

            for key in ['+', '-']:
                result = pd.DataFrame(columns=merge_field)
                for i in range(len(positioning) - 1):
                    if result.empty:
                        merge_df = positioning[i][key].merge(positioning[i + 1][key], how='outer', on=merge_field)
                        merge_df['sum_position'] = merge_df['actual_position_x'].fillna(0) + merge_df['actual_position_y'].fillna(0)
                        merge_df['sum_money'] = merge_df['position_money_x'].fillna(0) + merge_df['position_money_y'].fillna(0)
                    else:
                        merge_df = result.merge(positioning[i + 1][key], how='outer', on=merge_field)
                        merge_df['sum_position'] = merge_df['sum_position'].fillna(0) + merge_df['actual_position'].fillna(0)
                        merge_df['sum_money'] = merge_df['sum_money'].fillna(0) + merge_df['position_money'].fillna(0)
                    result = merge_df[merge_field + ['sum_position', 'sum_money']]
                # result['p_money_sum'] = result['sum_money'].sum()
                new_arr.append(result)

            res_ds = pd.concat([new_arr[0], new_arr[1]], ignore_index=True)
            cf = list(set(res_ds[res_ds.groupby('type_name_ab')['type_name_ab'].transform('count') > 1]['type_name_ab'].tolist()))
            # first_money = 0
            for val in cf:
                cf_col = res_ds[res_ds['type_name_ab'] == val]
                res_ds.loc[res_ds['type_name_ab'] == val, "sum_position"] = cf_col.iloc[0]['sum_position'] + cf_col.iloc[1]['sum_position']
                # first_money += cf_col.iloc[0]['sum_money'] + cf_col.iloc[1]['sum_money']
                res_ds.loc[res_ds['type_name_ab'] == val, "sum_money"] = cf_col.iloc[0]['sum_money'] + cf_col.iloc[1]['sum_money']

            res_ds.drop_duplicates(subset=['type_name_ab'], keep='first', inplace=True)
            res_ds['round_sum_position'] = round(res_ds['sum_position'])
            # res_ds['p_money_sum'] = res_ds['p_money_sum'].iloc[0] + first_money
            result = res_ds
            pass
        else:
            for key in ['+', '-']:
                result = positioning[0][key]
                new_arr.append(result)
            result = pd.concat([new_arr[0], new_arr[1]], ignore_index=True)

        return result


class FvSecAnalyPositioning(FvAnalysisBase, FactorPositioning, NightTrading):
    def cal_main(self):
        pass

    def init_data_processing(self):
        pass



