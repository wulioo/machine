import pandas as pd


class AxisMixin:
    _x: list
    _y: list
    _xy: list

    @property
    def xs(self):
        return self._x

    @property
    def ys(self):
        return self._y

    @property
    def xy(self):
        return self._xy

    def get_y_x_xy(self, df: pd.DataFrame, factor: list, label_ods: list) -> None:
        """
        获取坐标轴
        xy->因子+收益标签
        xs->因子
        ys->收益标签
        :param df:
        :param factor:
        :param label_ods:
        :return:
        """
        label_cols = [f'label_{i}' for i in label_ods]
        drop_cols = ['trading_date']
        if 'type_name_ab' in df:
            drop_cols.append('type_name_ab')

        if "wind_code" in df:
            drop_cols.append('wind_code')

        if "spread_name" in df:
            drop_cols.append('spread_name')

        xy = df.drop(columns=drop_cols)
        self._xy = xy.columns.tolist()
        self._x = df[factor].columns.tolist()
        self._y = df[label_cols].columns.tolist()
        # return [xy, x, y]
