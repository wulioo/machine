import os
from functools import lru_cache
from datetime import date, datetime

import pandas as pd


class TradingHoursData:
    def __init__(self):
        self._all_data = self._get_all_data()

    def _get_all_data(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trading_hours.csv")
        data = pd.read_csv(file_path)
        data.loc[:, "expiration_date"] = data.loc[:, "expiration_date"].apply(self._change_date_format)
        data.loc[:, "effective_date"] = data.loc[:, "effective_date"].apply(self._change_date_format)
        return data

    @staticmethod
    def _change_date_format(date_str: str):
        if pd.isna(date_str):
            date_data = date(9999, 12, 31)
        else:
            date_str = date_str.replace("-", "").replace("/", "")
            date_data = datetime.strptime(date_str, "%Y%m%d").date()
        return date_data

    @lru_cache()
    def is_night_trade(self, code: str, trading_date: date):
        code_filter = self._all_data.loc[:, "wind_code"] == code
        data = self._all_data.loc[code_filter]
        start_date_filter = data.loc[:, "effective_date"] <= trading_date
        data = data.loc[start_date_filter]
        end_date_filter = data.loc[:, "expiration_date"] >= trading_date
        data = data.loc[end_date_filter]
        if len(data) != 1:
            raise Exception(f"{code} {trading_date} 获取到的交易时间不为一个")
        return not pd.isna(data.iloc[0, :]["start_time4"])


trading_hours_data = TradingHoursData()

if __name__ == "__main__":
    # test_code = "A.DCE"
    # test_date1 = date(2014, 1, 3)
    # test_date2 = date(2014, 12, 27)
    # test_date3 = date(2015, 5, 9)
    # print(trading_hours_data.is_night_trade(test_code, test_date1))
    # print(trading_hours_data.is_night_trade(test_code, test_date2))
    # print(trading_hours_data.is_night_trade(test_code, test_date3))
    test_date1 = date(2022, 12, 7)
    for val in ['A.DCE', 'Y.DCE', 'ZN.SHF']:
        print(trading_hours_data.is_night_trade(val, test_date1))
