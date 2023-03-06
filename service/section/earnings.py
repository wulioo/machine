import json

import pandas as pd

from extra.db.models_tqmain import FutureHeader
from service.earnings import Earnings
from service.facotr_base import FvAnalysisBase
from service.factor import FutureFactor


class FvSecAnalyEarnings(FvAnalysisBase):
    def __init__(self, earn: Earnings, periods):
        self.__earn = earn
        self.__periods = periods
        super(FvSecAnalyEarnings, self).__init__()

    def cal_main(self):
        factor_df = self.init_data_processing()
        wc_and_erg = self.__earn.cal_earnings(factor_df, self.__periods)
        wc_and_erg.sort_values(by=['type_name_ab', 'trading_date'], ascending=[True, True], inplace=True, ignore_index=True)
        wc_and_erg['trading_date'] = wc_and_erg['trading_date'].astype(str)
        if self.__earn.cal_ear.sharpe:
            return_label = [f'sharpe_{val}' for val in self.__periods]
            wc_and_erg.rename(columns={f'label_{val}': f'sharpe_{val}' for val in self.__periods}, inplace=True)  # 通过key—value 修改列名称
            wc_and_erg[return_label] = wc_and_erg[return_label].round(8).fillna('')
        else:
            return_label = [f'return_{val}' for val in self.__periods]
            wc_and_erg.rename(columns={f'label_{val}': f'return_{val}' for val in self.__periods}, inplace=True)  # 通过key—value 修改列名称
            wc_and_erg[return_label] = (wc_and_erg[return_label] * 100).round(8).fillna('')

        return list(json.loads(wc_and_erg.T.to_json()).values())

    def init_data_processing(self):
        factor_df = self.get_fv_factor()
        return self.get_main_contracts(factor_df, self.get_type_name, 'right')

    def get_fv_factor(self):
        return pd.DataFrame(columns=['type_name_ab', 'trading_date'])

    @property
    def get_type_name(self):
        """
       根据 FutureHeader 表来获取type_name
       :param exchange_future:
       :return:
       """
        df = FutureHeader.get_duplication_field('type_name_ab', 'tqmain')
        df['exchange'] = df['type_name_ab'].str[-3:]
        return df[df['exchange'].isin(self.exchange)]['type_name_ab'].tolist()
