import pandas as pd
from django.db.models import Q

from extra.db.models_tqdailydrv import DwsTradingTimeFutureDaily
from utils.common import Common


class NightTrading:
    night = None

    def get_night_trading_type(self, df: pd.DataFrame):
        tds = df['trading_date'].unique().tolist()
        df_list = []
        for td in tds:
            # td_time = Common.get_previous_trading_time(td)
            nature_df = DwsTradingTimeFutureDaily.get_info_all(Q(trading_date=td), ['trading_date', 'type_name_ab', 'trading_time_list'], 'tq_daily_drv')
            nature_df['trading_time_list'] = nature_df['trading_time_list'].apply(lambda x: x[0][0] == '21:00:00')
            nature_df.drop(nature_df[nature_df['trading_time_list'] == False].index, inplace=True)
            n_type = nature_df['type_name_ab'].unique().tolist()
            td_non = df[(df['type_name_ab'].isin(n_type)) & (df['trading_date'] == td)]
            df_list.append(td_non)
        result = pd.concat(df_list, ignore_index=True)
        return result
