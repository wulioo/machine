import json
from abc import ABCMeta, abstractmethod

import pandas as pd

from extra.db.models_tqfactor import FvFactorInfo

from utils.common import Common


class TableNames(metaclass=ABCMeta):
    # @abstractmethod
    # def cal_icir(self, factor, factor_item, factor_diff, redis_key):
    #     pass

    # @abstractmethod
    # def cal_layered_test(self, factor, factor_item, redis_key):
    #     pass

    # @abstractmethod
    # def cal_ndcg(self, factor, factor_item):
    #     pass

    # @abstractmethod
    # def cal_corr(self, factor, factor_item):
    #     pass

    # @abstractmethod
    # def cal_review_corr(self, factor, file_df, factor_item, file_cols):
    #     pass
    #
    # @abstractmethod
    # def cal_box_muster_chart(self, factor, factor_item):
    #     pass

    # @abstractmethod
    # def cal_coverage(self, factor, factor_item):
    #     pass

    @abstractmethod
    def cal_positing(self, factor, factor_item, weight, money, type_name_ab):
        pass

    # @abstractmethod
    # def cal_sequential_icir(self, factor, factor_item):
    #     pass

    # @abstractmethod
    # def cal_backtesting(self, factor, factor_item):
    #     pass


class Table(TableNames):
    # def cal_icir(self, factor, factor_item, factor_diff, redis_key):
    #     result = []
    #     for table, future in factor_item.items():
    #         factor.model = Common.get_models('db', table)
    #         factor.column = future.get('factor_list')  # 因子
    #         type_name_ab = factor.get_typename_by_exchange()
    #         factor_df = factor.get_fv_factor(type_name_ab)
    #         factor_df = factor.get_night_trading_type(factor_df) if factor.night else factor_df
    #
    #         factor_df = factor.vari.fill_df_value(factor_df, factor.column)
    #         ic_data, summary_data = factor.cal_table_icir(factor_df, factor_diff)
    #         result.append({'ic': ic_data, 'summary': summary_data, 'table': table})
    #
    #     tmp_res = {}
    #     for res in result:
    #         data = factor.save_redis(res['table'], res['ic'], res['summary'], redis_key)
    #         tmp_res.update(data)
    #
    #     return tmp_res

    # def cal_layered_test(self, factor, factor_item, redis_key):
    #     result = dict()
    #     for table, future in factor_item.items():
    #         factor.model = Common.get_models('db', table)
    #         factor.column = future.get('factor_list')  # 因子列表
    #         type_name_ab = factor.get_typename_by_exchange()
    #         # 1.从因子库找到对应的因子字段 以及 wind_code 或者type_name_ab
    #         factor_df = factor.get_fv_factor(type_name_ab)
    #         factor_df = factor.get_night_trading_type(factor_df) if factor.night else factor_df
    #         factor_df = factor.vari.fill_df_value(factor_df, factor.column)
    #         result[table] = factor.layered_test(factor_df, table, redis_key)
    #     return result

    # def cal_ndcg(self, factor, factor_item):
    #     result = dict()
    #     for table, future in factor_item.items():
    #         factor.model = Common.get_models('db', table)
    #         factor.column = future.get('factor_list')  # 因子
    #         type_name_ab = factor.get_typename_by_exchange()
    #         factor_df = factor.get_fv_factor(type_name_ab)
    #         factor_df = factor.get_night_trading_type(factor_df) if factor.night else factor_df
    #         factor_df = factor.vari.fill_df_value(factor_df, factor.column)
    #         result[table] = factor.cal_ndcg(factor_df)
    #     return result

    # def cal_corr(self, factor, factor_item):
    #     tables = []
    #     for table, future in factor_item.items():
    #         factor.model = Common.get_models('db', table)
    #         factor.column = future.get('factor_list')  # 因子
    #
    #         factor_df = factor.get_factor_value()
    #         factor_df = factor.get_night_trading_type(factor_df) if factor.night else factor_df
    #         # 因子排名
    #         factor_df = factor.get_factor_sort(factor_df) if factor.sort else factor_df
    #
    #         tables.append(factor_df)
    #     factor_list = tables[0]
    #     if len(tables) > 1:
    #         for i in (range(len(tables) - 1)):
    #             factor_list = factor_list.merge(tables[i + 1], how="outer", on=['trading_date', factor.type_name])
    #     df = factor_list.drop(labels=['trading_date', factor.type_name], axis=1)
    #     return df.corr()

    # def cal_review_corr(self, factor, file_df, factor_item, file_cols):
    #     try:
    #         tables = []
    #         for table, future in factor_item.items():
    #             factor.model = Common.get_models('db', table)
    #             factor.column = future.get('factor_list')  # 因子
    #             factor_arr = factor.get_factor_value()
    #             factor_arr = factor.get_factor_sort(factor_arr) if factor.sort == 'true' else factor_arr
    #
    #             tables.append(factor_arr)
    #         factor_list = tables[0]
    #         if len(tables) > 1:
    #             for i in (range(len(tables) - 1)):
    #                 factor_list2 = tables[i + 1]
    #                 factor_list = factor_list.merge(factor_list2, how="outer", on=['trading_date', 'type_name_ab'])
    #         # 文件因子排序
    #         factor.column = file_cols
    #         file_df = factor.get_factor_sort(file_df) if factor.sort == 'true' else file_df
    #
    #         factor_list = file_df.merge(factor_list, how="outer", on=['trading_date', 'type_name_ab'])
    #         df = factor_list.drop(labels=['trading_date', 'type_name_ab'], axis=1)
    #     except Exception as e:
    #         df = file_df.drop(labels=['trading_date', 'type_name_ab'], axis=1)
    #
    #     result = df.corr()
    #     result = result[factor.column] if factor.sort == 'true' else result[file_cols]
    #     return result

    # def cal_box_muster_chart(self, factor, factor_item):
    #     data = {}
    #     for table, future in factor_item.items():
    #         factor.model = Common.get_models('db', table)
    #         factor.column = future.get('factor_list')  # 因子
    #         type_name_ab = factor.get_typename_by_exchange()
    #         factor_df = factor.get_factor_by_type(type_name_ab)
    #         factor_df = factor.get_night_trading_type(factor_df) if factor.night else factor_df
    #         factor_df = factor.box_chart_factor_sort(factor_df) if factor.sort else factor_df
    #         data[table] = factor.celery_box_muster_chart(factor_df)
    #     return data
    #
    # def cal_coverage(self, factor, factor_item):
    #     table_df = pd.DataFrame(columns=['trading_date', 'type_name_ab'])
    #     for table, future in factor_item.items():
    #         factor.model = Common.get_models('db', table)
    #         factor.column = future.get('factor_list')  # 因子
    #         type_name_ab = factor.get_typename_by_exchange()
    #         factor_df = factor.get_factor_by_type(type_name_ab)
    #         factor_df = factor.get_night_trading_type(factor_df) if factor.night else factor_df
    #         table_df = table_df.merge(factor_df, how='outer', on=['trading_date', 'type_name_ab'])
    #     result = factor.cal_coverage(table_df)
    #     return result

    def cal_positing(self, factor, factor_item, weight, money, type_name_ab):
        result = dict()
        for table, future in factor_item.items():
            factor.model = Common.get_models('db', table)
            positioning = {}
            factor_list = future.get('factor_list')
            for f_col in factor_list:
                factor.column = f_col  # 因子
                factor.weight = float(weight[table][f_col])  # 权重
                factor.layered.money = money * factor.weight / 100  # 金额
                positioning[f_col] = factor.cal_positioning(type_name_ab)
            data = factor.many_factor_merge(list(positioning.values()))
            res = {}
            for key, val in positioning.items():
                new_arr = []
                for short_long, sl_data in val.items():
                    new_arr.append(sl_data)
                res[key] = list(json.loads(pd.concat([new_arr[0], new_arr[1]], ignore_index=True).T.to_json()).values())
            result[table] = {
                'summary': list(json.loads(data.T.to_json()).values()),
                'single': res
            }

        return result

    # def cal_sequential_icir(self, factor, factor_item):
    #     result = {}
    #     for table, future in factor_item.items():
    #         factor.model = Common.get_models('db', table)
    #         factor.column = future.get('factor_list')  # 因子
    #         result[table] = factor.cal_main_functions()
    #     return result

    # def cal_backtesting(self, factor, factor_item):
    #     result = dict()
    #     for table, future in factor_item.items():
    #         factor.model = Common.get_models('db', table)
    #         factor.column = future.get('factor_list')  # 因子列表
    #         type_name_ab = factor.get_typename_by_exchange()
    #         # 1.从因子库找到对应的因子字段 以及 wind_code 或者type_name_ab
    #         factor_df = factor.get_fv_factor(type_name_ab)
    #         factor_df = factor.get_night_trading_type(factor_df) if factor.night else factor_df
    #         result[table] = factor.layered_backtesting(factor_df)
    #     return result


class Category(TableNames):

    def __get_factor_by_category(self, factor_item):
        result = {}
        for ca_one_name, category_one in factor_item.items():
            for ca_two_name, factor_list in category_one.items():
                table_list = Common.get_table(factor_list)
                combined_keys = result.keys() | table_list.keys()
                result.update({key: result.get(key, []) + table_list.get(key, []) for key in combined_keys})

        return dict(sorted(result.items(), key=lambda x: x[0]))

    def __category_merge_factor(self, factor, factor_item):
        factor_merge = pd.DataFrame(columns=['trading_date', 'wind_code', 'type_name_ab'])
        factor_item = self.__get_factor_by_category(factor_item)
        for table, tf_list in factor_item.items():
            factor.model = Common.get_models('db', table)
            factor.column = tf_list
            type_name_ab = factor.get_typename_by_exchange()
            # 1.从因子库找到对应的因子字段 以及 wind_code 或者type_name_ab
            factor_df = factor.get_fv_factor(type_name_ab)

            # factor_df.drop(['type_name_ab'], axis=1, inplace=True)
            factor_merge = factor_merge.merge(factor_df, how="outer", on=['trading_date', 'wind_code', 'type_name_ab'])
        factor_merge = factor.get_night_trading_type(factor_merge) if factor.night else factor_merge
        factor_merge.drop(['type_name_ab'], axis=1, inplace=True)
        return factor_merge

    # def __category_merge_corr(self, factor, factor_item):
    #     factor_merge = pd.DataFrame(columns=['trading_date', 'type_name_ab'])
    #     factor_item = self.__get_factor_by_category(factor_item)
    #     for table, tf_list in factor_item.items():
    #         factor.model = Common.get_models('db', table)
    #         factor.column = tf_list
    #         factor_df = factor.get_factor_value()
    #         factor_merge = factor_merge.merge(factor_df, how="outer", on=['trading_date', 'type_name_ab'])
    #     factor_merge = factor.get_night_trading_type(factor_merge) if factor.night else factor_merge
    #     return factor_merge

    # def cal_icir(self, factor, factor_item, factor_diff, redis_key):
    #     factor_df = self.__category_merge_factor(factor, factor_item)
    #     factor.column = factor_df.drop(['wind_code', 'trading_date'], axis=1).columns.tolist()
    #
    #     factor_df = factor.vari.fill_df_value(factor_df, factor.column)
    #
    #     ic_data, summary_data = factor.cal_table_icir(factor_df, factor_diff)
    #     data = factor.save_redis('fv_factor_all_temp', ic_data, summary_data, redis_key)
    #
    #     return data

    # def cal_layered_test(self, factor, factor_item, redis_key):
    #     factor_df = self.__category_merge_factor(factor, factor_item)
    #     factor.column = factor_df.drop(['wind_code', 'trading_date'], axis=1).columns.tolist()
    #     factor_df = factor.vari.fill_df_value(factor_df, factor.column)
    #
    #     result = factor.layered_test(factor_df, 'fv_factor_layered', redis_key)
    #     return {'fv_factor_layered': result}

    # def cal_ndcg(self, factor, factor_item):
    #     factor_df = self.__category_merge_factor(factor, factor_item)
    #     factor.column = factor_df.drop(['wind_code', 'trading_date'], axis=1).columns.tolist()
    #     factor_df = factor.vari.fill_df_value(factor_df, factor.column)
    #     result = factor.cal_ndcg(factor_df)
    #     return {'fv_factor_all_ndcg': result}

    # def cal_corr(self, factor, factor_item):
    #     factor_merge = self.__category_merge_corr(factor, factor_item)
    #     factor.column = factor_merge.drop([factor.type_name, 'trading_date'], axis=1).columns.tolist()
    #     factor_df = factor.get_factor_sort(factor_merge) if factor.sort else factor_merge
    #
    #     df = factor_df.drop(labels=['trading_date', factor.type_name], axis=1)
    #     return df.corr()

    # def cal_review_corr(self, factor, file_df, factor_item, file_cols):
    #     try:
    #         factor_merge = self.__category_merge_corr(factor, factor_item)
    #         factor.column = factor_merge.drop(['type_name_ab', 'trading_date'], axis=1).columns.tolist()
    #
    #         # 表排序
    #         if factor.sort == 'true':
    #             factor_merge = factor.get_factor_sort(factor_merge)
    #             factor.column = file_cols
    #             file_df = factor.get_factor_sort(file_df)
    #         factor_list = file_df.merge(factor_merge, how="outer", on=['trading_date', 'type_name_ab'])
    #         df = factor_list.drop(labels=['trading_date', 'type_name_ab'], axis=1)
    #     except Exception as e:
    #         df = file_df.drop(labels=['trading_date', 'type_name_ab'], axis=1)
    #
    #     result = df.corr()
    #     result = result[factor.column] if factor.sort == 'true' else result[file_cols]
    #     return result

    # def cal_box_muster_chart(self, factor, factor_item):
    #     factor_merge = pd.DataFrame(columns=['trading_date', 'type_name_ab'])
    #     factor_item = self.__get_factor_by_category(factor_item)
    #     for table, tf_list in factor_item.items():
    #         factor.column = tf_list
    #         factor.model = Common.get_models('db', table)
    #         type_name_ab = factor.get_typename_by_exchange()
    #         factor_df = factor.get_factor_by_type(type_name_ab)
    #         factor_merge = factor_merge.merge(factor_df, how="outer", on=['trading_date', 'type_name_ab'])
    #     factor.column = factor_merge.drop(['type_name_ab', 'trading_date'], axis=1).columns.tolist()
    #     factor_merge = factor.get_night_trading_type(factor_merge) if factor.night else factor_merge
    #     factor_merge = factor.box_chart_factor_sort(factor_merge) if factor.sort else factor_merge
    #
    #     factor_dict = factor.celery_box_muster_chart(factor_merge)
    #     # factor_dict = factor.single_box_muster_chart(factor_merge)
    #     return {'factor_distribute_chart': factor_dict}

    # def cal_coverage(self, factor, factor_item):
    #     factor_merge = pd.DataFrame(columns=['trading_date', 'type_name_ab'])
    #     factor_item = self.__get_factor_by_category(factor_item)
    #     for table, tf_list in factor_item.items():
    #         factor.column = tf_list
    #         factor.model = Common.get_models('db', table)
    #         type_name_ab = factor.get_typename_by_exchange()
    #         factor_df = factor.get_factor_by_type(type_name_ab)
    #         factor_merge = factor_merge.merge(factor_df, how='outer', on=['trading_date', 'type_name_ab'])
    #     factor_merge = factor.get_night_trading_type(factor_merge) if factor.night else factor_merge
    #
    #     result = factor.cal_coverage(factor_merge)
    #     return result

    # def cal_positing(self, factor, factor_item, weight, money, type_name_ab):
    #     factor_item = self.__get_factor_by_category(factor_item)
    #     dup_factor = FvFactorInfo.get_distinct_field('factor_name', 'tq_factor')
    #     positioning = {}
    #     for table, factor_list in factor_item.items():
    #         factor.model = Common.get_models('db', table)
    #         for f_col in factor_list:
    #             factor.column = f_col  # 因子
    #             if f_col in dup_factor:
    #                 f_col = f'{table}.{f_col}'
    #             factor.weight = float(weight[f_col])  # 权重
    #             factor.layered.money = money * factor.weight / 100  # 金额
    #             positioning[f_col] = factor.cal_positioning(type_name_ab)
    #     summary = factor.many_factor_merge(list(positioning.values()))
    #     res = {}
    #     for key, val in positioning.items():
    #         new_arr = []
    #         for short_long, sl_data in val.items():
    #             new_arr.append(sl_data)
    #         res[key] = list(json.loads(pd.concat([new_arr[0], new_arr[1]], ignore_index=True).T.to_json()).values())
    #     return {'temp_positioning': {
    #         'summary': list(json.loads(summary.T.to_json()).values()),
    #         'single': res
    #     }}

    # def cal_sequential_icir(self, factor, factor_item):
    #     factor_merge = pd.DataFrame(columns=['trading_date', 'type_name_ab', 'wind_code'])
    #     factor_item = self.__get_factor_by_category(factor_item)
    #     for table, tf_list in factor_item.items():
    #         factor.model = Common.get_models('db', table)
    #         factor.column = tf_list
    #         type_name_ab = factor.get_type_name
    #         # 1.从因子库找到对应的因子字段 以及 wind_code 或者type_name_ab
    #         factor_df = factor.get_fv_factor(type_name_ab)
    #         join_method = 'right' if factor.vari.vits != "all" else 'left'
    #         factor_df = factor.get_wd_by_type(factor_df, type_name_ab, join_method)
    #         factor_df = factor.vari.fill_df_value(factor_df, factor.column)
    #         factor_df.dropna(subset=['wind_code'], inplace=True)
    #         factor_merge = factor_merge.merge(factor_df, how="outer", on=['trading_date', 'type_name_ab', 'wind_code'])
    #     factor.column = factor_merge.drop(['type_name_ab', 'wind_code', 'trading_date'], axis=1).columns.tolist()
    #
    #     wc_and_erg = factor.earn.cal_earnings(factor_merge, factor.periods)
    #     type_name_ab = factor.get_type_name
    #     data = factor.celery_seq_ic(wc_and_erg, type_name_ab)
    #     return {"seq_factor_temp": data}

    # def cal_backtesting(self, factor, factor_item):
    #     factor_df = self.__category_merge_factor(factor, factor_item)
    #     factor.column = factor_df.drop(['wind_code', 'trading_date'], axis=1).columns.tolist()
    #     result = factor.layered_backtesting(factor_df)
    #     return {'fv_factor_backtesting': result}


