import json
import time
import warnings

import pandas as pd
from Machine.settings import BASE_DIR
from service.db import MysqlDb

warnings.filterwarnings('ignore')


class MonitorICIR:
    file_seq_path = f"{BASE_DIR}\static\\fixtures\\rolling_factor_list_flatform.json"
    file_sec_path = f"{BASE_DIR}\static\\fixtures\\rolling_factor_list_platform.json"

    def __init__(self):
        with open(self.file_sec_path, "r") as f:
            self._init_sec_data = json.loads(f.read())
        with open(self.file_seq_path, "r") as f:
            self._init_seq_data = json.loads(f.read())

    def _repeat_process(self, data):
        """重复因子查找表名"""
        info_df = self._fv_factor_info
        df_nan = data[pd.isnull(data['table_name']) == True].iloc[:, :1]
        df_dup = info_df[info_df.groupby('factor_name')['factor_name'].transform('count') > 1]
        dup_list = df_dup.drop_duplicates(subset=['factor_name'], keep='first', inplace=False)['factor_name'].values
        dup_merger = pd.DataFrame(columns=['factor_name', 'table_name'])
        for factor in dup_list:
            df_temp = df_dup[df_dup['factor_name'] == factor]
            x_df = df_temp.iloc[:1, :]
            x_df['factor_name'] = x_df['factor_name'] + '_x'
            y_df = df_temp.iloc[1:2, :]
            y_df['factor_name'] = y_df['factor_name'] + '_y'
            dup_merger = dup_merger.merge(pd.concat([x_df, y_df]), how='outer', on=['factor_name', 'table_name'])
        df_res = df_nan.merge(dup_merger, how="left", on='factor_name')
        data.dropna(subset='table_name', inplace=True)
        factor_df = pd.concat([df_res, data], ignore_index=True)
        factor_df['factor_name'] = factor_df['factor_name'].str.replace("_y", "")
        factor_df['factor_name'] = factor_df['factor_name'].str.replace("_x", "")
        return factor_df

    @property
    def _fv_factor_info(self):
        with MysqlDb() as db:
            sql = f"""select factor_name,table_name from fv_factor_info"""
            return pd.read_sql(sql, con=db.conn)

    def _insert_sec_ic_ir(self, val, is_night, label):
        create_time = time.strftime('%Y-%m-%d')
        return f""" insert into `tq_ml_sys`.`cm_sec_ic_ir` (`table`,factor,rank_ic,rank_ir,`status`,label,is_night,remarks,update_time,create_time)
                       values('{val['table_name']}','{val['factor_name']}',0.00,0.00,1,'label_{label}',{is_night},"",'{create_time}','{create_time}') """

    def _insert_seq_ic_ir(self, val, type, label):
        create_time = time.strftime('%Y-%m-%d')
        return f""" insert into `tq_ml_sys`.`cm_seq_ic_ir` (type_name_ab,`table`,factor,rank_ic,rank_ir,`status`,label,windows,remarks,update_time,create_time)
                           values('{type}','{val['table_name']}','{val['factor_name']}',0.00,0.00,1,'label_{label}',60,"",'{create_time}','{create_time}') """

    def sec_main(self, is_night: bool = False):
        for label, f_list in self._init_sec_data.items():
            factor_df = pd.DataFrame({'factor_name': f_list})
            data = self._fv_factor_info.merge(factor_df, how='right', on="factor_name")
            data = self._repeat_process(data)
            data['sql'] = data.apply(lambda x: self._insert_sec_ic_ir(x, is_night, label), axis=1)
            with MysqlDb() as db:
                db.insert_many_data(data['sql'])

    def seq_main(self, _time):
        for _type, t_val in self._init_seq_data.items():
            for _label, f_list in t_val[str(_time)].items():
                factor_df = pd.DataFrame({'factor_name': f_list})
                data = self._fv_factor_info.merge(factor_df, how='right', on="factor_name")
                data = self._repeat_process(data)
                data['sql'] = data.apply(lambda x: self._insert_seq_ic_ir(x, _type, _label), axis=1)
                with MysqlDb() as db:
                    db.insert_many_data(data['sql'])


if __name__ == '__main__':
    icir = MonitorICIR()
    icir.sec_main(True)
    icir.sec_main(False)
    icir.seq_main(4)
