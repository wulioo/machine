from typing import List

import pandas as pd
from django.db.models import Count


class BaseModel:
    @classmethod
    def get_info_all(cls, condtions, field: list = [], use_db: str = 'default') -> pd.DataFrame:
        model_obj = cls.objects.using(use_db).values(*field)
        if condtions:
            model_obj = model_obj.filter(condtions)

        return pd.DataFrame(model_obj)


    @classmethod
    def get_distinct_field(cls, field: str, use_db: str = 'default'):
        """获取重复字段"""
        model_obj = cls.objects.using(use_db).values(field)
        df = pd.DataFrame(model_obj)
        return df[df.groupby(field)[field].transform('count') > 1][field].tolist()

    @classmethod
    def get_duplication_field(cls, field: str, use_db: str = 'default'):
        """字段去重"""
        model_obj = cls.objects.using(use_db).values(field).distinct()

        return pd.DataFrame(model_obj)

    @classmethod
    def get_dup_field_by_condition(cls,condtions, field: str, use_db: str = 'default'):
        """字段去重"""
        model_obj = cls.objects.using(use_db).filter(condtions).values(field).distinct()

        return pd.DataFrame(model_obj)
    @classmethod
    def get_orderby_info_all(cls, condtions, field: list = List, orderby: list = List, use_db: str = 'default') -> pd.DataFrame:
        model_obj = cls.objects.using(use_db).values(*field)
        if condtions:
            model_obj = model_obj.filter(condtions)
        if len(orderby) > 1:
            model_obj.order_by(*orderby)
        return pd.DataFrame(model_obj)
