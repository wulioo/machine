import json
from abc import ABCMeta, abstractmethod

import pandas as pd

from extra.db.models_tqfactor import FvFactorInfo
from extra.db.models_tqsignal import FvSignalInfo
from utils.common import Common


class TableType(metaclass=ABCMeta):

    def __init__(self, factor):
        self.factor = factor
        self.factor.set_db(self._db)

    @abstractmethod
    def main(self, factor_item):
        pass

    @abstractmethod
    def cal_merge_factor(self, factor_item):
        pass

    @abstractmethod
    def cal_layered(self, factor_item, redis_key):
        pass


class SingleTable(TableType):
    def main(self, factor_item):
        result = {}
        for table, future in factor_item.items():
            self.factor.model = Common.get_models('db', table)
            self.factor.column = future.get('factor_list')  # 因子
            self.factor.df = self.factor.init_data_processing()
            result[table] = self.factor.cal_main()
        return result

    def cal_merge_factor(self, factor_item):
        self.factor.df = pd.DataFrame(columns=['trading_date', self.factor.type_name])
        for table, future in factor_item.items():
            self.factor.model = Common.get_models('db', table)
            self.factor.column = future.get('factor_list')  # 因子
            factor_df = self.factor.init_data_processing()
            self.factor.df = self.factor.df.merge(factor_df, how="outer", on=['trading_date', self.factor.type_name])
        return self.factor.cal_main()

    def cal_layered(self, factor_item, redis_key):
        result = dict()
        for table, future in factor_item.items():
            self.factor.model = Common.get_models('db', table)
            self.factor.column = future.get('factor_list')  # 因子列表
            self.factor.df = self.factor.init_data_processing()
            data = self.factor.cal_main()
            result[table] = self.factor.resp_layered(data, table, redis_key)
        return result

    def cal_positing(self, factor_item, weight, money, type_name_ab):
        self.factor.periods.set_db(self._db)
        result = dict()
        for table, future in factor_item.items():
            self.factor.model = Common.get_models('db', table)
            positioning = {}
            factor_list = future.get('factor_list')
            for f_col in factor_list:
                self.factor.column = f_col  # 因子
                self.factor.weight = float(weight[table][f_col])  # 权重
                self.factor.layered.money = money * self.factor.weight / 100  # 金额
                positioning[f_col] = self.factor.cal_positioning(type_name_ab)
            data = self.factor.many_factor_merge(list(positioning.values()))
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


class MultiTable(TableType):
    def _get_factor_by_category(self, factor_item):
        result = dict()
        for ca_one_name, category_one in factor_item.items():
            for ca_two_name, factor_list in category_one.items():
                table_list = Common.get_table(factor_list, self._db)
                combined_keys = result.keys() | table_list.keys()
                result.update({key: result.get(key, []) + table_list.get(key, []) for key in combined_keys})
        return dict(sorted(result.items(), key=lambda x: x[0]))

    def _get_merge_factor_data(self, factor_item):
        self.factor.df = pd.DataFrame(columns=['trading_date', 'type_name_ab', 'wind_code'])
        factor_item = self._get_factor_by_category(factor_item)
        for table, tf_list in factor_item.items():
            self.factor.model = Common.get_models('db', table)
            self.factor.column = tf_list
            factor_df = self.factor.init_data_processing()
            self.factor.df = self.factor.df.merge(factor_df, how="outer", on=['trading_date', 'type_name_ab', 'wind_code'])
        self.factor.column = self.factor.df.drop(['type_name_ab', 'wind_code', 'trading_date'], axis=1).columns.tolist()

    def main(self, factor_item):
        self._get_merge_factor_data(factor_item)
        data = self.factor.cal_main()
        return {"factor_temp": data}

    def cal_merge_factor(self, factor_item):
        self.factor.df = pd.DataFrame(columns=['trading_date', self.factor.type_name])
        factor_item = self._get_factor_by_category(factor_item)
        for table, tf_list in factor_item.items():
            self.factor.model = Common.get_models('db', table)
            self.factor.column = tf_list
            factor_df = self.factor.init_data_processing()
            self.factor.df = self.factor.df.merge(factor_df, how="outer", on=['trading_date', self.factor.type_name])
        return self.factor.cal_main()

    def cal_layered(self, factor_item, redis_key):
        self._get_merge_factor_data(factor_item)
        data = self.factor.cal_main()
        result = self.factor.resp_layered(data, 'fv_factor_layered', redis_key)
        return {'fv_factor_layered': result}

    def cal_positing(self, factor_item, weight, money, type_name_ab):
        self.factor.periods.set_db(self._db)
        factor_item = self._get_factor_by_category(factor_item)
        if self._db == "tq_factor":
            dup_factor = FvFactorInfo.get_distinct_field('factor_name', self._db)
        else:
            dup_factor = FvSignalInfo.get_distinct_field('factor_name', self._db)
        positioning = {}
        for table, factor_list in factor_item.items():
            self.factor.model = Common.get_models('db', table)
            for f_col in factor_list:
                self.factor.column = f_col  # 因子
                if f_col in dup_factor:
                    f_col = f'{table}.{f_col}'
                self.factor.weight = float(weight[f_col])  # 权重
                self.factor.layered.money = money * self.factor.weight / 100  # 金额
                positioning[f_col] = self.factor.cal_positioning(type_name_ab)
        summary = self.factor.many_factor_merge(list(positioning.values()))
        res = {}
        for key, val in positioning.items():
            new_arr = []
            for short_long, sl_data in val.items():
                new_arr.append(sl_data)
            res[key] = list(json.loads(pd.concat([new_arr[0], new_arr[1]], ignore_index=True).T.to_json()).values())
        return {'temp_positioning': {
            'summary': list(json.loads(summary.T.to_json()).values()),
            'single': res
        }}


class FactorSingleTable(SingleTable):
    _db = 'tq_factor'


class FactorMultiTable(MultiTable):
    _db = 'tq_factor'


class SignalSingleTable(SingleTable):
    _db = 'tq_signal'


class SignalMultiTable(MultiTable):
    _db = 'tq_signal'
