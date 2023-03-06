# import pandas as pd
#
# from service.varieties import Varieties
#
#
# class DataCleaning:
#     df: pd.DataFrame
#     exchange: list
#     vari: Varieties
#
#     @property
#     def get_type_name(self):
#         """
#         根据 交易所 表来获取type_name_ab
#         :return:
#         """
#         # df = self.model.get_duplication_field('type_name_ab', 'tq_factor')
#         self.df['exchange'] = self.df['type_name_ab'].str[-3:]
#         type_name_ab = self.df[self.df['exchange'].isin(self.exchange)]['type_name_ab'].tolist()
#         return type_name_ab
#
#     def init_data_clear(self):
#         """数据清洗"""
#         # type_name_ab = self.get_type_name
#         # factor_arr = self.get_fv_factor(type_name_ab)
#         factor_arr = self.vari.fill_df_value(self.df, self.column)
#         return factor_arr
