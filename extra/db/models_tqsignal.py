from extra.db.base_model import BaseModel  # This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FvSignalInfo(models.Model, BaseModel):
    factor_id = models.AutoField(primary_key=True)
    factor_name = models.CharField(max_length=64)
    table_name = models.CharField(max_length=64)
    warehousing_date = models.DateField()
    category1 = models.CharField(max_length=20, blank=True, null=True)
    category2 = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_signal_info'
        unique_together = (('table_name', 'factor_name'),)


class SignalCategoryInfo(models.Model,BaseModel):
    category_id = models.PositiveIntegerField(primary_key=True)
    pid = models.PositiveIntegerField()
    category_name = models.CharField(max_length=20)
    instrument_type = models.CharField(max_length=20)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'signal_category_info'

class Fv1DAi10(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v400_day_return_10_rank = models.FloatField(blank=True, null=True)
    v400_day_return_10_rank_mxm = models.FloatField(blank=True, null=True)
    v400_day_return_5_rank = models.FloatField(blank=True, null=True)
    v400_day_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v400_day_sharpe_10_rank = models.FloatField(blank=True, null=True)
    v400_day_sharpe_10_rank_mxm = models.FloatField(blank=True, null=True)
    v400_day_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v400_day_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v400_eve0_return_1_rank = models.FloatField(blank=True, null=True)
    v400_eve0_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v400_eve0_return_2_rank = models.FloatField(blank=True, null=True)
    v400_eve0_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v400_eve0_return_3_rank = models.FloatField(blank=True, null=True)
    v400_eve0_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v400_eve0_return_5_rank = models.FloatField(blank=True, null=True)
    v400_eve0_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v400_eve0_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v400_eve0_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v400_eve_return_1_rank = models.FloatField(blank=True, null=True)
    v400_eve_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v400_eve_return_2_rank = models.FloatField(blank=True, null=True)
    v400_eve_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v400_eve_return_3_rank = models.FloatField(blank=True, null=True)
    v400_eve_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v400_eve_return_5_rank = models.FloatField(blank=True, null=True)
    v400_eve_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v400_eve_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v400_eve_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_10'
        unique_together = (('trading_date', 'type_name_ab'),)

class Fv1DAi11(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v401_day_return_10_rank = models.FloatField(blank=True, null=True)
    v401_day_return_10_rank_mxm = models.FloatField(blank=True, null=True)
    v401_day_return_5_rank = models.FloatField(blank=True, null=True)
    v401_day_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v401_day_sharpe_10_rank = models.FloatField(blank=True, null=True)
    v401_day_sharpe_10_rank_mxm = models.FloatField(blank=True, null=True)
    v401_day_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v401_day_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v401_eve0_return_1_rank = models.FloatField(blank=True, null=True)
    v401_eve0_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v401_eve0_return_2_rank = models.FloatField(blank=True, null=True)
    v401_eve0_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v401_eve0_return_3_rank = models.FloatField(blank=True, null=True)
    v401_eve0_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v401_eve0_return_5_rank = models.FloatField(blank=True, null=True)
    v401_eve0_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v401_eve0_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v401_eve0_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v401_eve_return_1_rank = models.FloatField(blank=True, null=True)
    v401_eve_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v401_eve_return_2_rank = models.FloatField(blank=True, null=True)
    v401_eve_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v401_eve_return_3_rank = models.FloatField(blank=True, null=True)
    v401_eve_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v401_eve_return_5_rank = models.FloatField(blank=True, null=True)
    v401_eve_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v401_eve_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v401_eve_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_11'
        unique_together = (('trading_date', 'type_name_ab'),)

class Fv1DAi12(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v402_day_return_10_rank = models.FloatField(blank=True, null=True)
    v402_day_return_10_rank_mxm = models.FloatField(blank=True, null=True)
    v402_day_return_5_rank = models.FloatField(blank=True, null=True)
    v402_day_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v402_day_sharpe_10_rank = models.FloatField(blank=True, null=True)
    v402_day_sharpe_10_rank_mxm = models.FloatField(blank=True, null=True)
    v402_day_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v402_day_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v402_eve0_return_1_rank = models.FloatField(blank=True, null=True)
    v402_eve0_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v402_eve0_return_2_rank = models.FloatField(blank=True, null=True)
    v402_eve0_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v402_eve0_return_3_rank = models.FloatField(blank=True, null=True)
    v402_eve0_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v402_eve0_return_5_rank = models.FloatField(blank=True, null=True)
    v402_eve0_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v402_eve0_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v402_eve0_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v402_eve_return_1_rank = models.FloatField(blank=True, null=True)
    v402_eve_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v402_eve_return_2_rank = models.FloatField(blank=True, null=True)
    v402_eve_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v402_eve_return_3_rank = models.FloatField(blank=True, null=True)
    v402_eve_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v402_eve_return_5_rank = models.FloatField(blank=True, null=True)
    v402_eve_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v402_eve_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v402_eve_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_12'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAi13(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v403_day_return_10_rank = models.FloatField(blank=True, null=True)
    v403_day_return_10_rank_mxm = models.FloatField(blank=True, null=True)
    v403_day_return_5_rank = models.FloatField(blank=True, null=True)
    v403_day_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v403_day_sharpe_10_rank = models.FloatField(blank=True, null=True)
    v403_day_sharpe_10_rank_mxm = models.FloatField(blank=True, null=True)
    v403_day_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v403_day_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v403_eve0_return_1_rank = models.FloatField(blank=True, null=True)
    v403_eve0_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v403_eve0_return_2_rank = models.FloatField(blank=True, null=True)
    v403_eve0_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v403_eve0_return_3_rank = models.FloatField(blank=True, null=True)
    v403_eve0_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v403_eve0_return_5_rank = models.FloatField(blank=True, null=True)
    v403_eve0_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v403_eve0_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v403_eve0_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v403_eve_return_1_rank = models.FloatField(blank=True, null=True)
    v403_eve_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v403_eve_return_2_rank = models.FloatField(blank=True, null=True)
    v403_eve_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v403_eve_return_3_rank = models.FloatField(blank=True, null=True)
    v403_eve_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v403_eve_return_5_rank = models.FloatField(blank=True, null=True)
    v403_eve_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v403_eve_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v403_eve_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_13'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAi14(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v404_day_return_10_rank = models.FloatField(blank=True, null=True)
    v404_day_return_10_rank_mxm = models.FloatField(blank=True, null=True)
    v404_day_return_5_rank = models.FloatField(blank=True, null=True)
    v404_day_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v404_day_sharpe_10_rank = models.FloatField(blank=True, null=True)
    v404_day_sharpe_10_rank_mxm = models.FloatField(blank=True, null=True)
    v404_day_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v404_day_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v404_eve0_return_1_rank = models.FloatField(blank=True, null=True)
    v404_eve0_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v404_eve0_return_2_rank = models.FloatField(blank=True, null=True)
    v404_eve0_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v404_eve0_return_3_rank = models.FloatField(blank=True, null=True)
    v404_eve0_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v404_eve0_return_5_rank = models.FloatField(blank=True, null=True)
    v404_eve0_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v404_eve0_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v404_eve0_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v404_eve_return_1_rank = models.FloatField(blank=True, null=True)
    v404_eve_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v404_eve_return_2_rank = models.FloatField(blank=True, null=True)
    v404_eve_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v404_eve_return_3_rank = models.FloatField(blank=True, null=True)
    v404_eve_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v404_eve_return_5_rank = models.FloatField(blank=True, null=True)
    v404_eve_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v404_eve_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v404_eve_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_14'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAi15(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v405_day_return_10_rank = models.FloatField(blank=True, null=True)
    v405_day_return_10_rank_mxm = models.FloatField(blank=True, null=True)
    v405_day_return_5_rank = models.FloatField(blank=True, null=True)
    v405_day_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v405_day_sharpe_10_rank = models.FloatField(blank=True, null=True)
    v405_day_sharpe_10_rank_mxm = models.FloatField(blank=True, null=True)
    v405_day_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v405_day_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v405_eve0_return_1_rank = models.FloatField(blank=True, null=True)
    v405_eve0_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v405_eve0_return_2_rank = models.FloatField(blank=True, null=True)
    v405_eve0_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v405_eve0_return_3_rank = models.FloatField(blank=True, null=True)
    v405_eve0_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v405_eve0_return_5_rank = models.FloatField(blank=True, null=True)
    v405_eve0_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v405_eve0_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v405_eve0_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v405_eve_return_1_rank = models.FloatField(blank=True, null=True)
    v405_eve_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v405_eve_return_2_rank = models.FloatField(blank=True, null=True)
    v405_eve_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v405_eve_return_3_rank = models.FloatField(blank=True, null=True)
    v405_eve_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v405_eve_return_5_rank = models.FloatField(blank=True, null=True)
    v405_eve_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v405_eve_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v405_eve_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_15'
        unique_together = (('trading_date', 'type_name_ab'),)

