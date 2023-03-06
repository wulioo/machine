from extra.db.base_model import BaseModel# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Fv1DBasis1(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    basis_mom_5 = models.FloatField(blank=True, null=True)
    basis_mom_10 = models.FloatField(blank=True, null=True)
    basis_mom_15 = models.FloatField(blank=True, null=True)
    basis_mom_20 = models.FloatField(blank=True, null=True)
    basis_mom_30 = models.FloatField(blank=True, null=True)
    basis_mom_60 = models.FloatField(blank=True, null=True)
    ts_slope_5 = models.FloatField(blank=True, null=True)
    ts_slope_10 = models.FloatField(blank=True, null=True)
    ts_slope_15 = models.FloatField(blank=True, null=True)
    ts_slope_20 = models.FloatField(blank=True, null=True)
    ts_slope_30 = models.FloatField(blank=True, null=True)
    ts_slope_60 = models.FloatField(blank=True, null=True)
    carry_5 = models.FloatField(blank=True, null=True)
    carry_10 = models.FloatField(blank=True, null=True)
    carry_15 = models.FloatField(blank=True, null=True)
    carry_20 = models.FloatField(blank=True, null=True)
    carry_30 = models.FloatField(blank=True, null=True)
    carry_60 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_basis_1'
        unique_together = (('trading_date', 'type_name_ab'),)


class Eq1DAi1(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    wind_code = models.CharField(max_length=20)
    f_3years = models.FloatField(blank=True, null=True)
    f_3years_open905 = models.FloatField(blank=True, null=True)
    f_9features_mostyears_open905_window47 = models.FloatField(blank=True, null=True)
    f_11years_open905_window47 = models.FloatField(blank=True, null=True)
    f_11years_window47_10days = models.FloatField(blank=True, null=True)
    f_mostyears_open905_window47 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'eq_1d_ai_1'
        unique_together = (('trading_date', 'wind_code'),)


class Eq1DAi2(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    wind_code = models.CharField(max_length=20)
    f_l1_11years_day47minute10_vwap5m905_1day = models.FloatField(blank=True, null=True)
    f_l1_11years_day47minute10_vwap5m905_5days = models.FloatField(blank=True, null=True)
    f_l1_11years_vwap5m905_1day = models.FloatField(blank=True, null=True)
    f_l1_11years_vwap5m905_5days = models.FloatField(blank=True, null=True)
    f_l1_flat_11years_day47minute5_vwap5m905_5days = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'eq_1d_ai_2'
        unique_together = (('trading_date', 'wind_code'),)


class Eq1DAi3(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    wind_code = models.CharField(max_length=20)
    f_l1_11years_day47minute5_vwap5m905_5days = models.FloatField(blank=True, null=True)
    f_l1_flat_11years_day47minute5_vwap5m905_1day = models.FloatField(blank=True, null=True)
    f_l1_flat_11years_day47minute10_vwap5m905_5days = models.FloatField(blank=True, null=True)
    f_l1_flat_11years_vwap5m905_5days = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'eq_1d_ai_3'
        unique_together = (('trading_date', 'wind_code'),)


class Eq1DAi4(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    wind_code = models.CharField(max_length=20)
    f_11years_open905 = models.FloatField(blank=True, null=True)
    f_mostyears_open905 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'eq_1d_ai_4'
        unique_together = (('trading_date', 'wind_code'),)


class Eq1DAlpha(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    wind_code = models.CharField(max_length=20)
    value = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'eq_1d_alpha'
        unique_together = (('trading_date', 'wind_code'),)


class Eq1DVolprice1(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    wind_code = models.CharField(max_length=20)
    jor = models.FloatField(blank=True, null=True)
    alpha10 = models.FloatField(blank=True, null=True)
    long_mom = models.FloatField(blank=True, null=True)
    scr = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'eq_1d_volprice_1'
        unique_together = (('trading_date', 'wind_code'),)


class Equity1MVolprice(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    wind_code = models.CharField(max_length=20)
    ykws_1 = models.FloatField(blank=True, null=True)
    ykws_2 = models.FloatField(blank=True, null=True)
    ykws_3 = models.FloatField(blank=True, null=True)
    sdmx_1 = models.FloatField(blank=True, null=True)
    sdmx_2 = models.FloatField(blank=True, null=True)
    wzcx_1 = models.FloatField(blank=True, null=True)
    wzcx_2 = models.FloatField(blank=True, null=True)
    wzcx_3 = models.FloatField(blank=True, null=True)
    intraday = models.FloatField(blank=True, null=True)
    m_vol = models.FloatField(blank=True, null=True)
    mvolume_1 = models.FloatField(blank=True, null=True)
    mvolume_2 = models.FloatField(blank=True, null=True)
    mvolume_3 = models.FloatField(blank=True, null=True)
    mvolume_4 = models.FloatField(blank=True, null=True)
    mvolume_5 = models.FloatField(blank=True, null=True)
    mprice_1 = models.FloatField(blank=True, null=True)
    mprice_2 = models.FloatField(blank=True, null=True)
    mprice_gmm_1 = models.FloatField(blank=True, null=True)
    mprice_gmm_2 = models.FloatField(blank=True, null=True)
    mprice_gmm_3 = models.FloatField(blank=True, null=True)
    mprice_gmm_4 = models.FloatField(blank=True, null=True)
    up_vol = models.FloatField(blank=True, null=True)
    min_corr = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'equity_1m_volprice'
        unique_together = (('trading_date', 'wind_code'),)


class FactorCategoryInfo(models.Model,BaseModel):
    category_id = models.PositiveIntegerField(primary_key=True)
    pid = models.PositiveIntegerField()
    category_name = models.CharField(max_length=20)
    instrument_type = models.CharField(max_length=20)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'factor_category_info'


class FinanceCategoryFactor(models.Model,BaseModel):
    wind_code = models.CharField(primary_key=True, max_length=10)
    trading_date = models.DateField()
    earning_factor = models.FloatField(blank=True, null=True)
    growth_factor = models.FloatField(blank=True, null=True)
    security_factor = models.FloatField(blank=True, null=True)
    operation_factor = models.FloatField(blank=True, null=True)
    value_factor = models.FloatField(blank=True, null=True)
    combine_factor = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'finance_category_factor'
        unique_together = (('wind_code', 'trading_date'),)


class FutureQuantityPriceDailyFactor(models.Model,BaseModel):
    wind_code = models.CharField(max_length=20)
    trading_date = models.DateField(primary_key=True)
    pre_oi = models.FloatField(blank=True, null=True)
    pre_volume = models.FloatField(blank=True, null=True)
    pre_amount = models.FloatField(blank=True, null=True)
    pre_long_margin = models.FloatField(blank=True, null=True)
    pre_short_margin = models.FloatField(blank=True, null=True)
    mth_num = models.FloatField(blank=True, null=True)
    day_num = models.FloatField(blank=True, null=True)
    weekday_num = models.FloatField(blank=True, null=True)
    c_pct_change = models.FloatField(blank=True, null=True)
    oi_pct_change = models.FloatField(blank=True, null=True)
    v_pct_change = models.FloatField(blank=True, null=True)
    m_pct_change = models.FloatField(blank=True, null=True)
    s_pct_change = models.FloatField(blank=True, null=True)
    marl_change = models.FloatField(blank=True, null=True)
    mars_change = models.FloatField(blank=True, null=True)
    cs_diff = models.FloatField(blank=True, null=True)
    hl_diff = models.FloatField(blank=True, null=True)
    co_diff = models.FloatField(blank=True, null=True)
    vwap = models.FloatField(blank=True, null=True)
    marls_diff = models.FloatField(blank=True, null=True)
    free_turn = models.FloatField(blank=True, null=True)
    preclose_2od = models.FloatField(blank=True, null=True)
    preclose_5od = models.FloatField(blank=True, null=True)
    preclose_10od = models.FloatField(blank=True, null=True)
    preclose_20od = models.FloatField(blank=True, null=True)
    return_1od = models.FloatField(blank=True, null=True)
    return_2od = models.FloatField(blank=True, null=True)
    return_5od = models.FloatField(blank=True, null=True)
    return_10od = models.FloatField(blank=True, null=True)
    return_20od = models.FloatField(blank=True, null=True)
    low_p_1od = models.FloatField(blank=True, null=True)
    low_p_2od = models.FloatField(blank=True, null=True)
    low_p_5od = models.FloatField(blank=True, null=True)
    low_p_10od = models.FloatField(blank=True, null=True)
    low_p_20od = models.FloatField(blank=True, null=True)
    drawdown_1od = models.FloatField(blank=True, null=True)
    drawdown_2od = models.FloatField(blank=True, null=True)
    drawdown_5od = models.FloatField(blank=True, null=True)
    drawdown_10od = models.FloatField(blank=True, null=True)
    drawdown_20od = models.FloatField(blank=True, null=True)
    high_p_1od = models.FloatField(blank=True, null=True)
    high_p_2od = models.FloatField(blank=True, null=True)
    high_p_5od = models.FloatField(blank=True, null=True)
    high_p_10od = models.FloatField(blank=True, null=True)
    high_p_20od = models.FloatField(blank=True, null=True)
    drawup_1od = models.FloatField(blank=True, null=True)
    drawup_2od = models.FloatField(blank=True, null=True)
    drawup_5od = models.FloatField(blank=True, null=True)
    drawup_10od = models.FloatField(blank=True, null=True)
    drawup_20od = models.FloatField(blank=True, null=True)
    vol_2od = models.FloatField(blank=True, null=True)
    vol_5od = models.FloatField(blank=True, null=True)
    vol_10od = models.FloatField(blank=True, null=True)
    vol_20od = models.FloatField(blank=True, null=True)
    return_voladj_1od = models.FloatField(blank=True, null=True)
    return_voladj_2od = models.FloatField(blank=True, null=True)
    return_voladj_5od = models.FloatField(blank=True, null=True)
    return_voladj_10od = models.FloatField(blank=True, null=True)
    return_voladj_20od = models.FloatField(blank=True, null=True)
    high_price_percentile_3 = models.FloatField(blank=True, null=True)
    high_price_percentile_5 = models.FloatField(blank=True, null=True)
    high_price_percentile_10 = models.FloatField(blank=True, null=True)
    high_price_percentile_15 = models.FloatField(blank=True, null=True)
    high_price_percentile_20 = models.FloatField(blank=True, null=True)
    low_price_percentile_3 = models.FloatField(blank=True, null=True)
    low_price_percentile_5 = models.FloatField(blank=True, null=True)
    low_price_percentile_10 = models.FloatField(blank=True, null=True)
    low_price_percentile_15 = models.FloatField(blank=True, null=True)
    low_price_percentile_20 = models.FloatField(blank=True, null=True)
    close_price_percentile_3 = models.FloatField(blank=True, null=True)
    close_price_percentile_5 = models.FloatField(blank=True, null=True)
    close_price_percentile_10 = models.FloatField(blank=True, null=True)
    close_price_percentile_15 = models.FloatField(blank=True, null=True)
    close_price_percentile_20 = models.FloatField(blank=True, null=True)
    settle_percentile_3 = models.FloatField(blank=True, null=True)
    settle_percentile_5 = models.FloatField(blank=True, null=True)
    settle_percentile_10 = models.FloatField(blank=True, null=True)
    settle_percentile_15 = models.FloatField(blank=True, null=True)
    settle_percentile_20 = models.FloatField(blank=True, null=True)
    volume_percentile_3 = models.FloatField(blank=True, null=True)
    volume_percentile_5 = models.FloatField(blank=True, null=True)
    volume_percentile_10 = models.FloatField(blank=True, null=True)
    volume_percentile_15 = models.FloatField(blank=True, null=True)
    volume_percentile_20 = models.FloatField(blank=True, null=True)
    amount_percentile_3 = models.FloatField(blank=True, null=True)
    amount_percentile_5 = models.FloatField(blank=True, null=True)
    amount_percentile_10 = models.FloatField(blank=True, null=True)
    amount_percentile_15 = models.FloatField(blank=True, null=True)
    amount_percentile_20 = models.FloatField(blank=True, null=True)
    oi_percentile_3 = models.FloatField(blank=True, null=True)
    oi_percentile_5 = models.FloatField(blank=True, null=True)
    oi_percentile_10 = models.FloatField(blank=True, null=True)
    oi_percentile_15 = models.FloatField(blank=True, null=True)
    oi_percentile_20 = models.FloatField(blank=True, null=True)
    high_price_minmax_3 = models.FloatField(blank=True, null=True)
    high_price_minmax_5 = models.FloatField(blank=True, null=True)
    high_price_minmax_10 = models.FloatField(blank=True, null=True)
    high_price_minmax_15 = models.FloatField(blank=True, null=True)
    high_price_minmax_20 = models.FloatField(blank=True, null=True)
    low_price_minmax_3 = models.FloatField(blank=True, null=True)
    low_price_minmax_5 = models.FloatField(blank=True, null=True)
    low_price_minmax_10 = models.FloatField(blank=True, null=True)
    low_price_minmax_15 = models.FloatField(blank=True, null=True)
    low_price_minmax_20 = models.FloatField(blank=True, null=True)
    close_price_minmax_3 = models.FloatField(blank=True, null=True)
    close_price_minmax_5 = models.FloatField(blank=True, null=True)
    close_price_minmax_10 = models.FloatField(blank=True, null=True)
    close_price_minmax_15 = models.FloatField(blank=True, null=True)
    close_price_minmax_20 = models.FloatField(blank=True, null=True)
    settle_minmax_3 = models.FloatField(blank=True, null=True)
    settle_minmax_5 = models.FloatField(blank=True, null=True)
    settle_minmax_10 = models.FloatField(blank=True, null=True)
    settle_minmax_15 = models.FloatField(blank=True, null=True)
    settle_minmax_20 = models.FloatField(blank=True, null=True)
    volume_minmax_3 = models.FloatField(blank=True, null=True)
    volume_minmax_5 = models.FloatField(blank=True, null=True)
    volume_minmax_10 = models.FloatField(blank=True, null=True)
    volume_minmax_15 = models.FloatField(blank=True, null=True)
    volume_minmax_20 = models.FloatField(blank=True, null=True)
    amount_minmax_3 = models.FloatField(blank=True, null=True)
    amount_minmax_5 = models.FloatField(blank=True, null=True)
    amount_minmax_10 = models.FloatField(blank=True, null=True)
    amount_minmax_15 = models.FloatField(blank=True, null=True)
    amount_minmax_20 = models.FloatField(blank=True, null=True)
    oi_minmax_3 = models.FloatField(blank=True, null=True)
    oi_minmax_5 = models.FloatField(blank=True, null=True)
    oi_minmax_10 = models.FloatField(blank=True, null=True)
    oi_minmax_15 = models.FloatField(blank=True, null=True)
    oi_minmax_20 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'future_quantity_price_daily_factor'
        unique_together = (('trading_date', 'wind_code'),)


class FutureTechDailyFactor(models.Model,BaseModel):
    wind_code = models.CharField(max_length=20)
    trading_date = models.DateField(primary_key=True)
    atr_3 = models.FloatField(blank=True, null=True)
    atr_5 = models.FloatField(blank=True, null=True)
    atr_10 = models.FloatField(blank=True, null=True)
    atr_15 = models.FloatField(blank=True, null=True)
    atr_20 = models.FloatField(blank=True, null=True)
    bias_3 = models.FloatField(blank=True, null=True)
    bias_5 = models.FloatField(blank=True, null=True)
    bias_10 = models.FloatField(blank=True, null=True)
    bias_15 = models.FloatField(blank=True, null=True)
    bias_20 = models.FloatField(blank=True, null=True)
    kama_20 = models.FloatField(blank=True, null=True)
    linear_angle_3 = models.FloatField(blank=True, null=True)
    linear_angle_5 = models.FloatField(blank=True, null=True)
    linear_angle_10 = models.FloatField(blank=True, null=True)
    linear_angle_15 = models.FloatField(blank=True, null=True)
    linear_angle_20 = models.FloatField(blank=True, null=True)
    linear_inter_3 = models.FloatField(blank=True, null=True)
    linear_inter_5 = models.FloatField(blank=True, null=True)
    linear_inter_10 = models.FloatField(blank=True, null=True)
    linear_inter_15 = models.FloatField(blank=True, null=True)
    linear_inter_20 = models.FloatField(blank=True, null=True)
    linear_slope_3 = models.FloatField(blank=True, null=True)
    linear_slope_5 = models.FloatField(blank=True, null=True)
    linear_slope_10 = models.FloatField(blank=True, null=True)
    linear_slope_15 = models.FloatField(blank=True, null=True)
    linear_slope_20 = models.FloatField(blank=True, null=True)
    macd = models.FloatField(blank=True, null=True)
    macd_dea = models.FloatField(blank=True, null=True)
    macd_dif = models.FloatField(blank=True, null=True)
    mfi_5 = models.FloatField(blank=True, null=True)
    mfi_10 = models.FloatField(blank=True, null=True)
    mfi_20 = models.FloatField(blank=True, null=True)
    mom_3 = models.FloatField(blank=True, null=True)
    mom_5 = models.FloatField(blank=True, null=True)
    mom_10 = models.FloatField(blank=True, null=True)
    mom_15 = models.FloatField(blank=True, null=True)
    mom_20 = models.FloatField(blank=True, null=True)
    obv = models.FloatField(blank=True, null=True)
    psy_5 = models.FloatField(blank=True, null=True)
    psy_10 = models.FloatField(blank=True, null=True)
    psy_20 = models.FloatField(blank=True, null=True)
    rsi_5 = models.FloatField(blank=True, null=True)
    rsi_10 = models.FloatField(blank=True, null=True)
    rsi_20 = models.FloatField(blank=True, null=True)
    kdj_k_5 = models.FloatField(blank=True, null=True)
    kdj_k_10 = models.FloatField(blank=True, null=True)
    kdj_k_20 = models.FloatField(blank=True, null=True)
    kdj_d_5 = models.FloatField(blank=True, null=True)
    kdj_d_10 = models.FloatField(blank=True, null=True)
    kdj_d_20 = models.FloatField(blank=True, null=True)
    kdj_j_5 = models.FloatField(blank=True, null=True)
    kdj_j_10 = models.FloatField(blank=True, null=True)
    kdj_j_20 = models.FloatField(blank=True, null=True)
    corr_vh_3 = models.FloatField(blank=True, null=True)
    corr_vh_5 = models.FloatField(blank=True, null=True)
    corr_vh_10 = models.FloatField(blank=True, null=True)
    corr_vh_15 = models.FloatField(blank=True, null=True)
    corr_vh_20 = models.FloatField(blank=True, null=True)
    fac_s2 = models.FloatField(blank=True, null=True)
    fac_rng = models.FloatField(blank=True, null=True)
    corr_cv_3 = models.FloatField(blank=True, null=True)
    corr_cv_5 = models.FloatField(blank=True, null=True)
    corr_cv_10 = models.FloatField(blank=True, null=True)
    corr_cv_15 = models.FloatField(blank=True, null=True)
    corr_cv_20 = models.FloatField(blank=True, null=True)
    corr_hl_3 = models.FloatField(blank=True, null=True)
    corr_hl_5 = models.FloatField(blank=True, null=True)
    corr_hl_10 = models.FloatField(blank=True, null=True)
    corr_hl_15 = models.FloatField(blank=True, null=True)
    corr_hl_20 = models.FloatField(blank=True, null=True)
    illiq = models.FloatField(blank=True, null=True)
    illiq_avg_3 = models.FloatField(blank=True, null=True)
    illiq_avg_5 = models.FloatField(blank=True, null=True)
    illiq_avg_10 = models.FloatField(blank=True, null=True)
    illiq_avg_15 = models.FloatField(blank=True, null=True)
    illiq_avg_20 = models.FloatField(blank=True, null=True)
    volavg_3 = models.FloatField(db_column='volAvg_3', blank=True, null=True)  # Field name made lowercase.
    volavg_5 = models.FloatField(db_column='volAvg_5', blank=True, null=True)  # Field name made lowercase.
    volavg_10 = models.FloatField(db_column='volAvg_10', blank=True, null=True)  # Field name made lowercase.
    volavg_15 = models.FloatField(db_column='volAvg_15', blank=True, null=True)  # Field name made lowercase.
    volavg_20 = models.FloatField(db_column='volAvg_20', blank=True, null=True)  # Field name made lowercase.
    volvolatility_3 = models.FloatField(db_column='volVolatility_3', blank=True, null=True)  # Field name made lowercase.
    volvolatility_5 = models.FloatField(db_column='volVolatility_5', blank=True, null=True)  # Field name made lowercase.
    volvolatility_10 = models.FloatField(db_column='volVolatility_10', blank=True, null=True)  # Field name made lowercase.
    volvolatility_15 = models.FloatField(db_column='volVolatility_15', blank=True, null=True)  # Field name made lowercase.
    volvolatility_20 = models.FloatField(db_column='volVolatility_20', blank=True, null=True)  # Field name made lowercase.
    weightmom_3 = models.FloatField(db_column='weightMOM_3', blank=True, null=True)  # Field name made lowercase.
    weightmom_5 = models.FloatField(db_column='weightMOM_5', blank=True, null=True)  # Field name made lowercase.
    weightmom_10 = models.FloatField(db_column='weightMOM_10', blank=True, null=True)  # Field name made lowercase.
    weightmom_15 = models.FloatField(db_column='weightMOM_15', blank=True, null=True)  # Field name made lowercase.
    weightmom_20 = models.FloatField(db_column='weightMOM_20', blank=True, null=True)  # Field name made lowercase.
    volratio_1_20 = models.FloatField(db_column='volRatio_1_20', blank=True, null=True)  # Field name made lowercase.
    volratio_3_20 = models.FloatField(db_column='volRatio_3_20', blank=True, null=True)  # Field name made lowercase.
    volratio_5_20 = models.FloatField(db_column='volRatio_5_20', blank=True, null=True)  # Field name made lowercase.
    volratio_10_20 = models.FloatField(db_column='volRatio_10_20', blank=True, null=True)  # Field name made lowercase.
    cov_ft_c_3 = models.FloatField(blank=True, null=True)
    cov_ft_c_5 = models.FloatField(blank=True, null=True)
    cov_ft_c_10 = models.FloatField(blank=True, null=True)
    cov_ft_c_15 = models.FloatField(blank=True, null=True)
    cov_ft_c_20 = models.FloatField(blank=True, null=True)
    cov_ft_m_3 = models.FloatField(blank=True, null=True)
    cov_ft_m_5 = models.FloatField(blank=True, null=True)
    cov_ft_m_10 = models.FloatField(blank=True, null=True)
    cov_ft_m_15 = models.FloatField(blank=True, null=True)
    cov_ft_m_20 = models.FloatField(blank=True, null=True)
    mth_turn_avg_1 = models.FloatField(blank=True, null=True)
    turn_std_1 = models.FloatField(blank=True, null=True)
    turn_avg_3 = models.FloatField(blank=True, null=True)
    turn_avg_5 = models.FloatField(blank=True, null=True)
    turn_avg_10 = models.FloatField(blank=True, null=True)
    turn_avg_15 = models.FloatField(blank=True, null=True)
    turn_avg_20 = models.FloatField(blank=True, null=True)
    turnover_ratio_1_20 = models.FloatField(blank=True, null=True)
    turnover_ratio_3_20 = models.FloatField(blank=True, null=True)
    turnover_ratio_5_20 = models.FloatField(blank=True, null=True)
    turnover_ratio_10_20 = models.FloatField(blank=True, null=True)
    volatility_3 = models.FloatField(blank=True, null=True)
    volatility_5 = models.FloatField(blank=True, null=True)
    volatility_10 = models.FloatField(blank=True, null=True)
    volatility_15 = models.FloatField(blank=True, null=True)
    volatility_20 = models.FloatField(blank=True, null=True)
    volatility_ratio_3_20 = models.FloatField(blank=True, null=True)
    volatility_ratio_5_20 = models.FloatField(blank=True, null=True)
    volatility_ratio_10_20 = models.FloatField(blank=True, null=True)
    returnover20 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'future_tech_daily_factor'
        unique_together = (('trading_date', 'wind_code'),)


class FutureVarietiesDaily(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    pre_close = models.FloatField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.FloatField(blank=True, null=True)
    close_price = models.FloatField(blank=True, null=True)
    vwap = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    open_interest = models.FloatField(blank=True, null=True)
    return_field = models.FloatField(db_column='return', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    free_turn = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'future_varieties_daily'
        unique_together = (('trading_date', 'type_name_ab'),)


class FutureVarietiesDailyBak(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=50)
    wind_code = models.CharField(max_length=50)
    pre_close = models.FloatField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.FloatField(blank=True, null=True)
    close_price = models.FloatField(blank=True, null=True)
    vwap = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    open_interest = models.FloatField(blank=True, null=True)
    return_field = models.FloatField(db_column='return', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    free_turn = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'future_varieties_daily_bak'
        unique_together = (('trading_date', 'type_name_ab'),)


class FutureVarietiesTechDaily(models.Model,BaseModel):
    type_name_ab = models.CharField(max_length=45)
    trading_date = models.DateField(primary_key=True)
    atr_3 = models.FloatField(blank=True, null=True)
    atr_5 = models.FloatField(blank=True, null=True)
    atr_10 = models.FloatField(blank=True, null=True)
    atr_15 = models.FloatField(blank=True, null=True)
    atr_20 = models.FloatField(blank=True, null=True)
    bias_3 = models.FloatField(blank=True, null=True)
    bias_5 = models.FloatField(blank=True, null=True)
    bias_10 = models.FloatField(blank=True, null=True)
    bias_15 = models.FloatField(blank=True, null=True)
    bias_20 = models.FloatField(blank=True, null=True)
    kama_30 = models.FloatField(blank=True, null=True)
    kama_60 = models.FloatField(blank=True, null=True)
    kama_90 = models.FloatField(blank=True, null=True)
    linear_angle_3 = models.FloatField(blank=True, null=True)
    linear_angle_5 = models.FloatField(blank=True, null=True)
    linear_angle_10 = models.FloatField(blank=True, null=True)
    linear_angle_15 = models.FloatField(blank=True, null=True)
    linear_angle_20 = models.FloatField(blank=True, null=True)
    linear_inter_3 = models.FloatField(blank=True, null=True)
    linear_inter_5 = models.FloatField(blank=True, null=True)
    linear_inter_10 = models.FloatField(blank=True, null=True)
    linear_inter_15 = models.FloatField(blank=True, null=True)
    linear_inter_20 = models.FloatField(blank=True, null=True)
    linear_slope_3 = models.FloatField(blank=True, null=True)
    linear_slope_5 = models.FloatField(blank=True, null=True)
    linear_slope_10 = models.FloatField(blank=True, null=True)
    linear_slope_15 = models.FloatField(blank=True, null=True)
    linear_slope_20 = models.FloatField(blank=True, null=True)
    macd = models.FloatField(blank=True, null=True)
    macd_dea = models.FloatField(blank=True, null=True)
    macd_dif = models.FloatField(blank=True, null=True)
    mfi_6 = models.FloatField(blank=True, null=True)
    mfi_12 = models.FloatField(blank=True, null=True)
    mfi_24 = models.FloatField(blank=True, null=True)
    mom_3 = models.FloatField(blank=True, null=True)
    mom_5 = models.FloatField(blank=True, null=True)
    mom_10 = models.FloatField(blank=True, null=True)
    mom_15 = models.FloatField(blank=True, null=True)
    mom_20 = models.FloatField(blank=True, null=True)
    obv = models.FloatField(blank=True, null=True)
    psy_6 = models.FloatField(blank=True, null=True)
    psy_12 = models.FloatField(blank=True, null=True)
    psy_24 = models.FloatField(blank=True, null=True)
    rsi_6 = models.FloatField(blank=True, null=True)
    rsi_12 = models.FloatField(blank=True, null=True)
    rsi_24 = models.FloatField(blank=True, null=True)
    kdj_k_6 = models.FloatField(blank=True, null=True)
    kdj_k_12 = models.FloatField(blank=True, null=True)
    kdj_k_24 = models.FloatField(blank=True, null=True)
    kdj_d_6 = models.FloatField(blank=True, null=True)
    kdj_d_12 = models.FloatField(blank=True, null=True)
    kdj_d_24 = models.FloatField(blank=True, null=True)
    kdj_j_6 = models.FloatField(blank=True, null=True)
    kdj_j_12 = models.FloatField(blank=True, null=True)
    kdj_j_24 = models.FloatField(blank=True, null=True)
    corr_vh_3 = models.FloatField(blank=True, null=True)
    corr_vh_5 = models.FloatField(blank=True, null=True)
    corr_vh_10 = models.FloatField(blank=True, null=True)
    corr_vh_15 = models.FloatField(blank=True, null=True)
    corr_vh_20 = models.FloatField(blank=True, null=True)
    dcphase_0 = models.FloatField(db_column='DCPHASE__0', blank=True, null=True)  # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    httrend_0 = models.FloatField(db_column='HTTrend__0', blank=True, null=True)  # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    fac_s2 = models.FloatField(blank=True, null=True)
    fac_rng = models.FloatField(blank=True, null=True)
    corr_cv_3 = models.FloatField(blank=True, null=True)
    corr_cv_5 = models.FloatField(blank=True, null=True)
    corr_cv_10 = models.FloatField(blank=True, null=True)
    corr_cv_15 = models.FloatField(blank=True, null=True)
    corr_cv_20 = models.FloatField(blank=True, null=True)
    corr_hl_3 = models.FloatField(blank=True, null=True)
    corr_hl_5 = models.FloatField(blank=True, null=True)
    corr_hl_10 = models.FloatField(blank=True, null=True)
    corr_hl_15 = models.FloatField(blank=True, null=True)
    corr_hl_20 = models.FloatField(blank=True, null=True)
    illiq = models.FloatField(blank=True, null=True)
    illiq_avg_3 = models.FloatField(blank=True, null=True)
    illiq_avg_5 = models.FloatField(blank=True, null=True)
    illiq_avg_10 = models.FloatField(blank=True, null=True)
    illiq_avg_15 = models.FloatField(blank=True, null=True)
    illiq_avg_20 = models.FloatField(blank=True, null=True)
    volavg_3 = models.FloatField(db_column='volAvg_3', blank=True, null=True)  # Field name made lowercase.
    volavg_5 = models.FloatField(db_column='volAvg_5', blank=True, null=True)  # Field name made lowercase.
    volavg_10 = models.FloatField(db_column='volAvg_10', blank=True, null=True)  # Field name made lowercase.
    volavg_15 = models.FloatField(db_column='volAvg_15', blank=True, null=True)  # Field name made lowercase.
    volavg_20 = models.FloatField(db_column='volAvg_20', blank=True, null=True)  # Field name made lowercase.
    volvolatility_3 = models.FloatField(db_column='volVolatility_3', blank=True, null=True)  # Field name made lowercase.
    volvolatility_5 = models.FloatField(db_column='volVolatility_5', blank=True, null=True)  # Field name made lowercase.
    volvolatility_10 = models.FloatField(db_column='volVolatility_10', blank=True, null=True)  # Field name made lowercase.
    volvolatility_15 = models.FloatField(db_column='volVolatility_15', blank=True, null=True)  # Field name made lowercase.
    volvolatility_20 = models.FloatField(db_column='volVolatility_20', blank=True, null=True)  # Field name made lowercase.
    weightmom_3 = models.FloatField(db_column='weightMOM_3', blank=True, null=True)  # Field name made lowercase.
    weightmom_5 = models.FloatField(db_column='weightMOM_5', blank=True, null=True)  # Field name made lowercase.
    weightmom_10 = models.FloatField(db_column='weightMOM_10', blank=True, null=True)  # Field name made lowercase.
    weightmom_15 = models.FloatField(db_column='weightMOM_15', blank=True, null=True)  # Field name made lowercase.
    weightmom_20 = models.FloatField(db_column='weightMOM_20', blank=True, null=True)  # Field name made lowercase.
    volratio_1_20 = models.FloatField(db_column='volRatio_1_20', blank=True, null=True)  # Field name made lowercase.
    volratio_1_40 = models.FloatField(db_column='volRatio_1_40', blank=True, null=True)  # Field name made lowercase.
    volratio_1_60 = models.FloatField(db_column='volRatio_1_60', blank=True, null=True)  # Field name made lowercase.
    volratio_1_120 = models.FloatField(db_column='volRatio_1_120', blank=True, null=True)  # Field name made lowercase.
    volratio_3_20 = models.FloatField(db_column='volRatio_3_20', blank=True, null=True)  # Field name made lowercase.
    volratio_3_40 = models.FloatField(db_column='volRatio_3_40', blank=True, null=True)  # Field name made lowercase.
    volratio_3_60 = models.FloatField(db_column='volRatio_3_60', blank=True, null=True)  # Field name made lowercase.
    volratio_3_120 = models.FloatField(db_column='volRatio_3_120', blank=True, null=True)  # Field name made lowercase.
    volratio_5_20 = models.FloatField(db_column='volRatio_5_20', blank=True, null=True)  # Field name made lowercase.
    volratio_5_40 = models.FloatField(db_column='volRatio_5_40', blank=True, null=True)  # Field name made lowercase.
    volratio_5_60 = models.FloatField(db_column='volRatio_5_60', blank=True, null=True)  # Field name made lowercase.
    volratio_5_120 = models.FloatField(db_column='volRatio_5_120', blank=True, null=True)  # Field name made lowercase.
    volratio_10_20 = models.FloatField(db_column='volRatio_10_20', blank=True, null=True)  # Field name made lowercase.
    volratio_10_40 = models.FloatField(db_column='volRatio_10_40', blank=True, null=True)  # Field name made lowercase.
    volratio_10_60 = models.FloatField(db_column='volRatio_10_60', blank=True, null=True)  # Field name made lowercase.
    volratio_10_120 = models.FloatField(db_column='volRatio_10_120', blank=True, null=True)  # Field name made lowercase.
    cov_ft_c_3 = models.FloatField(blank=True, null=True)
    cov_ft_c_5 = models.FloatField(blank=True, null=True)
    cov_ft_c_10 = models.FloatField(blank=True, null=True)
    cov_ft_c_15 = models.FloatField(blank=True, null=True)
    cov_ft_c_20 = models.FloatField(blank=True, null=True)
    cov_ft_m_3 = models.FloatField(blank=True, null=True)
    cov_ft_m_5 = models.FloatField(blank=True, null=True)
    cov_ft_m_10 = models.FloatField(blank=True, null=True)
    cov_ft_m_15 = models.FloatField(blank=True, null=True)
    cov_ft_m_20 = models.FloatField(blank=True, null=True)
    mth_turn_avg_1 = models.FloatField(blank=True, null=True)
    mth_turn_avg_3 = models.FloatField(blank=True, null=True)
    mth_turn_avg_6 = models.FloatField(blank=True, null=True)
    mth_turn_avg_12 = models.FloatField(blank=True, null=True)
    turn_std_1 = models.FloatField(blank=True, null=True)
    turn_std_3 = models.FloatField(blank=True, null=True)
    turn_std_6 = models.FloatField(blank=True, null=True)
    turn_std_12 = models.FloatField(blank=True, null=True)
    turn_avg_3 = models.FloatField(blank=True, null=True)
    turn_avg_5 = models.FloatField(blank=True, null=True)
    turn_avg_10 = models.FloatField(blank=True, null=True)
    turn_avg_15 = models.FloatField(blank=True, null=True)
    turn_avg_20 = models.FloatField(blank=True, null=True)
    turnover_ratio_1_20 = models.FloatField(blank=True, null=True)
    turnover_ratio_1_40 = models.FloatField(blank=True, null=True)
    turnover_ratio_1_60 = models.FloatField(blank=True, null=True)
    turnover_ratio_1_120 = models.FloatField(blank=True, null=True)
    turnover_ratio_3_20 = models.FloatField(blank=True, null=True)
    turnover_ratio_3_40 = models.FloatField(blank=True, null=True)
    turnover_ratio_3_60 = models.FloatField(blank=True, null=True)
    turnover_ratio_3_120 = models.FloatField(blank=True, null=True)
    turnover_ratio_5_20 = models.FloatField(blank=True, null=True)
    turnover_ratio_5_40 = models.FloatField(blank=True, null=True)
    turnover_ratio_5_60 = models.FloatField(blank=True, null=True)
    turnover_ratio_5_120 = models.FloatField(blank=True, null=True)
    turnover_ratio_10_20 = models.FloatField(blank=True, null=True)
    turnover_ratio_10_40 = models.FloatField(blank=True, null=True)
    turnover_ratio_10_60 = models.FloatField(blank=True, null=True)
    turnover_ratio_10_120 = models.FloatField(blank=True, null=True)
    volatility_3 = models.FloatField(blank=True, null=True)
    volatility_5 = models.FloatField(blank=True, null=True)
    volatility_10 = models.FloatField(blank=True, null=True)
    volatility_15 = models.FloatField(blank=True, null=True)
    volatility_20 = models.FloatField(blank=True, null=True)
    mth_volatility_1 = models.FloatField(blank=True, null=True)
    mth_volatility_3 = models.FloatField(blank=True, null=True)
    mth_volatility_6 = models.FloatField(blank=True, null=True)
    mth_volatility_12 = models.FloatField(blank=True, null=True)
    volatility_ratio_3_20 = models.FloatField(blank=True, null=True)
    volatility_ratio_3_40 = models.FloatField(blank=True, null=True)
    volatility_ratio_3_60 = models.FloatField(blank=True, null=True)
    volatility_ratio_3_120 = models.FloatField(blank=True, null=True)
    volatility_ratio_5_20 = models.FloatField(blank=True, null=True)
    volatility_ratio_5_40 = models.FloatField(blank=True, null=True)
    volatility_ratio_5_60 = models.FloatField(blank=True, null=True)
    volatility_ratio_5_120 = models.FloatField(blank=True, null=True)
    volatility_ratio_10_20 = models.FloatField(blank=True, null=True)
    volatility_ratio_10_40 = models.FloatField(blank=True, null=True)
    volatility_ratio_10_60 = models.FloatField(blank=True, null=True)
    volatility_ratio_10_120 = models.FloatField(blank=True, null=True)
    returnover_20 = models.FloatField(blank=True, null=True)
    returnover_40 = models.FloatField(blank=True, null=True)
    returnover_60 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'future_varieties_tech_daily'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAi1(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v130_mlp_sect_ret_5d = models.FloatField(blank=True, null=True)
    v130_mlp_sect_ret_10d = models.FloatField(blank=True, null=True)
    v131_mlp_pca_sect_ret_5d = models.FloatField(blank=True, null=True)
    v131_mlp_pca_sect_ret_10d = models.FloatField(blank=True, null=True)
    v132_mlp_sect_rank_5d = models.FloatField(blank=True, null=True)
    v132_mlp_sect_rank_10d = models.FloatField(blank=True, null=True)
    v134_dpr_mlp_sect_ret_5d = models.FloatField(blank=True, null=True)
    v134_dpr_mlp_sect_ret_10d = models.FloatField(blank=True, null=True)
    v135_dpr_mlp_pca_sect_ret_5d = models.FloatField(blank=True, null=True)
    v135_dpr_mlp_pca_sect_ret_10d = models.FloatField(blank=True, null=True)
    v136_dpr_mlp_sect_rank_5d = models.FloatField(blank=True, null=True)
    v136_dpr_mlp_sect_rank_10d = models.FloatField(blank=True, null=True)
    v140_gbdt_sect_ret_5d = models.FloatField(blank=True, null=True)
    v140_gbdt_sect_ret_10d = models.FloatField(blank=True, null=True)
    v141_gbdt_pca_sect_ret_5d = models.FloatField(blank=True, null=True)
    v141_gbdt_pca_sect_ret_10d = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_1'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAi2(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v150_mlp1_sect_sharpe_5d = models.FloatField(blank=True, null=True)
    v150_mlp1_sect_sharpe_10d = models.FloatField(blank=True, null=True)
    v152_mlp2_sect_sharpe_5d = models.FloatField(blank=True, null=True)
    v152_mlp2_sect_sharpe_10d = models.FloatField(blank=True, null=True)
    v153_mlp3_sect_sharpe_5d = models.FloatField(blank=True, null=True)
    v153_mlp3_sect_sharpe_10d = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_2'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAi3(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    sec_v200_return_1d = models.FloatField(blank=True, null=True)
    sec_v200_r_rank_1d = models.FloatField(blank=True, null=True)
    sec_v200_return_3d = models.FloatField(blank=True, null=True)
    sec_v200_r_rank_3d = models.FloatField(blank=True, null=True)
    sec_v200_return_5d = models.FloatField(blank=True, null=True)
    sec_v200_sharpe_5d = models.FloatField(blank=True, null=True)
    sec_v200_r_rank_5d = models.FloatField(blank=True, null=True)
    sec_v200_return_10d = models.FloatField(blank=True, null=True)
    sec_v200_sharpe_10d = models.FloatField(blank=True, null=True)
    sec_v200_r_rank_10d = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_3'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAi4(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v302_return_1_rank = models.FloatField(blank=True, null=True)
    v302_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v302_return_3_rank = models.FloatField(blank=True, null=True)
    v302_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v302_return_5_rank = models.FloatField(blank=True, null=True)
    v302_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v302_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v302_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v302_return_10_rank = models.FloatField(blank=True, null=True)
    v302_return_10_rank_mxm = models.FloatField(blank=True, null=True)
    v302_sharpe_10_rank = models.FloatField(blank=True, null=True)
    v302_sharpe_10_rank_mxm = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_4'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAi5(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v306_return_1_rank = models.FloatField(blank=True, null=True)
    v306_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v306_return_2_rank = models.FloatField(blank=True, null=True)
    v306_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v306_return_3_rank = models.FloatField(blank=True, null=True)
    v306_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_5'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAi6(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v307_return_5_rank = models.FloatField(blank=True, null=True)
    v307_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v307_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v307_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v307_return_10_rank = models.FloatField(blank=True, null=True)
    v307_return_10_rank_mxm = models.FloatField(blank=True, null=True)
    v307_sharpe_10_rank = models.FloatField(blank=True, null=True)
    v307_sharpe_10_rank_mxm = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_6'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAi7(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v309_return_1_rank = models.FloatField(blank=True, null=True)
    v309_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v309_return_2_rank = models.FloatField(blank=True, null=True)
    v309_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v309_return_3_rank = models.FloatField(blank=True, null=True)
    v309_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v309_return_5_rank = models.FloatField(blank=True, null=True)
    v309_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v309_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v309_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v309_return_10_rank = models.FloatField(blank=True, null=True)
    v309_return_10_rank_mxm = models.FloatField(blank=True, null=True)
    v309_sharpe_10_rank = models.FloatField(blank=True, null=True)
    v309_sharpe_10_rank_mxm = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_7'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAi8(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v312_return_5_rank = models.FloatField(blank=True, null=True)
    v312_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v312_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v312_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v312_return_10_rank = models.FloatField(blank=True, null=True)
    v312_return_10_rank_mxm = models.FloatField(blank=True, null=True)
    v312_sharpe_10_rank = models.FloatField(blank=True, null=True)
    v312_sharpe_10_rank_mxm = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_8'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAi9(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v313_return_1_rank = models.FloatField(blank=True, null=True)
    v313_return_1_rank_mxm = models.FloatField(blank=True, null=True)
    v313_return_2_rank = models.FloatField(blank=True, null=True)
    v313_return_2_rank_mxm = models.FloatField(blank=True, null=True)
    v313_return_3_rank = models.FloatField(blank=True, null=True)
    v313_return_3_rank_mxm = models.FloatField(blank=True, null=True)
    v313_return_5_rank = models.FloatField(blank=True, null=True)
    v313_return_5_rank_mxm = models.FloatField(blank=True, null=True)
    v313_sharpe_5_rank = models.FloatField(blank=True, null=True)
    v313_sharpe_5_rank_mxm = models.FloatField(blank=True, null=True)
    v313_return_10_rank = models.FloatField(blank=True, null=True)
    v313_return_10_rank_mxm = models.FloatField(blank=True, null=True)
    v313_sharpe_10_rank = models.FloatField(blank=True, null=True)
    v313_sharpe_10_rank_mxm = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_9'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DAiCo1(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    v00_mlp_return_5d = models.FloatField(blank=True, null=True)
    v00_mlp_sharpe_5d = models.FloatField(blank=True, null=True)
    v00_mlp_r_rank_5d = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_ai_co_1'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DFundamental1(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    inventory1 = models.FloatField(blank=True, null=True)
    inventory2 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_fundamental_1'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DFundamental2(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    basis = models.FloatField(blank=True, null=True)
    standardized_basis = models.FloatField(blank=True, null=True)
    momentum = models.FloatField(blank=True, null=True)
    inventory = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_fundamental_2'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DFundamental3(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    momentum = models.FloatField(blank=True, null=True)
    basis = models.FloatField(blank=True, null=True)
    standardized_basis = models.FloatField(blank=True, null=True)
    inventory = models.FloatField(blank=True, null=True)
    estate = models.FloatField(blank=True, null=True)
    iron = models.FloatField(blank=True, null=True)
    zc_momentum = models.FloatField(blank=True, null=True)
    spread_zc_jm = models.FloatField(blank=True, null=True)
    term_structure = models.FloatField(blank=True, null=True)
    sc_momentum = models.FloatField(blank=True, null=True)
    spread_sc_bu = models.FloatField(blank=True, null=True)
    eg_inventory = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_fundamental_3'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DSection1(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    mom_5 = models.FloatField(blank=True, null=True)
    mom_10 = models.FloatField(blank=True, null=True)
    mom_15 = models.FloatField(blank=True, null=True)
    mom_20 = models.FloatField(blank=True, null=True)
    mom_25 = models.FloatField(blank=True, null=True)
    premium_5 = models.FloatField(blank=True, null=True)
    premium_10 = models.FloatField(blank=True, null=True)
    premium_15 = models.FloatField(blank=True, null=True)
    premium_20 = models.FloatField(blank=True, null=True)
    premium_25 = models.FloatField(blank=True, null=True)
    warehouse_receipt_5 = models.FloatField(blank=True, null=True)
    warehouse_receipt_10 = models.FloatField(blank=True, null=True)
    warehouse_receipt_15 = models.FloatField(blank=True, null=True)
    warehouse_receipt_20 = models.FloatField(blank=True, null=True)
    warehouse_receipt_25 = models.FloatField(blank=True, null=True)
    idio_vol_5 = models.FloatField(blank=True, null=True)
    idio_vol_10 = models.FloatField(blank=True, null=True)
    idio_vol_15 = models.FloatField(blank=True, null=True)
    idio_vol_20 = models.FloatField(blank=True, null=True)
    idio_vol_25 = models.FloatField(blank=True, null=True)
    volatility_5 = models.FloatField(blank=True, null=True)
    volatility_10 = models.FloatField(blank=True, null=True)
    volatility_15 = models.FloatField(blank=True, null=True)
    volatility_20 = models.FloatField(blank=True, null=True)
    volatility_25 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_section_1'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DSection2(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    net_position_top20_ma5_chg = models.FloatField(blank=True, null=True)
    net_position_top20_pct_ma_5 = models.FloatField(blank=True, null=True)
    LRSR_top20_ma_5 = models.FloatField(db_column='LRSR_top20_ma_5', blank=True, null=True)  # Field name made lowercase.
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_section_2'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DSection3(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    CPV_20 = models.FloatField(db_column='CPV_20', blank=True, null=True)  # Field name made lowercase.
    CPV_60 = models.FloatField(db_column='CPV_60', blank=True, null=True)  # Field name made lowercase.
    CPV_120 = models.FloatField(db_column='CPV_120', blank=True, null=True)  # Field name made lowercase.
    RCPV_5_10_60 = models.FloatField(db_column='RCPV_5_10_60', blank=True, null=True)  # Field name made lowercase.
    RCPV_5_20_60 = models.FloatField(db_column='RCPV_5_20_60', blank=True, null=True)  # Field name made lowercase.
    RCPV_5_30_60 = models.FloatField(db_column='RCPV_5_30_60', blank=True, null=True)  # Field name made lowercase.
    RCPV_10_10_60 = models.FloatField(db_column='RCPV_10_10_60', blank=True, null=True)  # Field name made lowercase.
    RCPV_10_20_60 = models.FloatField(db_column='RCPV_10_20_60', blank=True, null=True)  # Field name made lowercase.
    RCPV_10_30_60 = models.FloatField(db_column='RCPV_10_30_60', blank=True, null=True)  # Field name made lowercase.
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_section_3'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DSignal1(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    signal = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_signal_1'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DSignal2(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    momentum = models.IntegerField(blank=True, null=True)
    basis = models.IntegerField(blank=True, null=True)
    standardized_basis = models.IntegerField(blank=True, null=True)
    inventory = models.IntegerField(blank=True, null=True)
    estate = models.IntegerField(blank=True, null=True)
    iron = models.IntegerField(blank=True, null=True)
    zc_momentum = models.IntegerField(blank=True, null=True)
    spread_zc_jm = models.IntegerField(blank=True, null=True)
    term_structure = models.IntegerField(blank=True, null=True)
    sc_momentum = models.IntegerField(blank=True, null=True)
    spread_sc_bu = models.IntegerField(blank=True, null=True)
    eg_inventory = models.IntegerField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_signal_2'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DTech1(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    atr_3 = models.FloatField(blank=True, null=True)
    atr_5 = models.FloatField(blank=True, null=True)
    atr_10 = models.FloatField(blank=True, null=True)
    atr_15 = models.FloatField(blank=True, null=True)
    atr_20 = models.FloatField(blank=True, null=True)
    bias_3 = models.FloatField(blank=True, null=True)
    bias_5 = models.FloatField(blank=True, null=True)
    bias_10 = models.FloatField(blank=True, null=True)
    bias_15 = models.FloatField(blank=True, null=True)
    bias_20 = models.FloatField(blank=True, null=True)
    kama_30 = models.FloatField(blank=True, null=True)
    kama_60 = models.FloatField(blank=True, null=True)
    kama_90 = models.FloatField(blank=True, null=True)
    linear_angle_10 = models.FloatField(blank=True, null=True)
    linear_inter_3 = models.FloatField(blank=True, null=True)
    linear_inter_5 = models.FloatField(blank=True, null=True)
    linear_inter_10 = models.FloatField(blank=True, null=True)
    linear_inter_15 = models.FloatField(blank=True, null=True)
    linear_inter_20 = models.FloatField(blank=True, null=True)
    linear_slope_10 = models.FloatField(blank=True, null=True)
    macd_dif = models.FloatField(blank=True, null=True)
    mfi_6 = models.FloatField(blank=True, null=True)
    mfi_12 = models.FloatField(blank=True, null=True)
    mfi_24 = models.FloatField(blank=True, null=True)
    mom_5 = models.FloatField(blank=True, null=True)
    mom_10 = models.FloatField(blank=True, null=True)
    obv = models.FloatField(blank=True, null=True)
    psy_12 = models.FloatField(blank=True, null=True)
    psy_24 = models.FloatField(blank=True, null=True)
    rsi_6 = models.FloatField(blank=True, null=True)
    rsi_12 = models.FloatField(blank=True, null=True)
    rsi_24 = models.FloatField(blank=True, null=True)
    kdj_k_12 = models.FloatField(blank=True, null=True)
    kdj_k_24 = models.FloatField(blank=True, null=True)
    kdj_d_6 = models.FloatField(blank=True, null=True)
    kdj_d_12 = models.FloatField(blank=True, null=True)
    kdj_d_24 = models.FloatField(blank=True, null=True)
    kdj_j_6 = models.FloatField(blank=True, null=True)
    kdj_j_24 = models.FloatField(blank=True, null=True)
    corr_vh_10 = models.FloatField(blank=True, null=True)
    corr_vh_15 = models.FloatField(blank=True, null=True)
    corr_vh_20 = models.FloatField(blank=True, null=True)
    dcphase_0 = models.FloatField(db_column='DCPHASE__0', blank=True, null=True)  # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    httrend_0 = models.FloatField(db_column='HTTrend__0', blank=True, null=True)  # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    fac_s2 = models.FloatField(blank=True, null=True)
    fac_rng = models.FloatField(blank=True, null=True)
    corr_cv_20 = models.FloatField(blank=True, null=True)
    illiq = models.FloatField(blank=True, null=True)
    illiq_avg_10 = models.FloatField(blank=True, null=True)
    illiq_avg_15 = models.FloatField(blank=True, null=True)
    illiq_avg_20 = models.FloatField(blank=True, null=True)
    weightmom_3 = models.FloatField(db_column='weightMOM_3', blank=True, null=True)  # Field name made lowercase.
    cov_ft_c_20 = models.FloatField(blank=True, null=True)
    turn_std_6 = models.FloatField(blank=True, null=True)
    turn_std_12 = models.FloatField(blank=True, null=True)
    mth_volatility_12 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_tech_1'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DTech2(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    atr = models.FloatField(blank=True, null=True)
    exp_mom1_1 = models.FloatField(blank=True, null=True)
    exp_mom1_2 = models.FloatField(blank=True, null=True)
    exp_mom1_3 = models.FloatField(blank=True, null=True)
    exp_mom2_1 = models.FloatField(blank=True, null=True)
    exp_mom2_2 = models.FloatField(blank=True, null=True)
    exp_mom2_3 = models.FloatField(blank=True, null=True)
    mom = models.FloatField(blank=True, null=True)
    roll_ret1 = models.FloatField(blank=True, null=True)
    roll_ret2 = models.FloatField(blank=True, null=True)
    roll_ret3 = models.FloatField(blank=True, null=True)
    roll_avg = models.FloatField(blank=True, null=True)
    roll = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_tech_2'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DVolprice1(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    co_diff = models.FloatField(blank=True, null=True)
    return_1od = models.FloatField(blank=True, null=True)
    return_5od = models.FloatField(blank=True, null=True)
    return_10od = models.FloatField(blank=True, null=True)
    drawup_5od = models.FloatField(blank=True, null=True)
    drawup_10od = models.FloatField(blank=True, null=True)
    return_voladj_2od = models.FloatField(blank=True, null=True)
    return_voladj_5od = models.FloatField(blank=True, null=True)
    return_voladj_10od = models.FloatField(blank=True, null=True)
    return_voladj_20od = models.FloatField(blank=True, null=True)
    close_price_percentile_3 = models.FloatField(blank=True, null=True)
    close_price_percentile_5 = models.FloatField(blank=True, null=True)
    close_price_percentile_10 = models.FloatField(blank=True, null=True)
    high_price_minmax_15 = models.FloatField(blank=True, null=True)
    high_price_minmax_20 = models.FloatField(blank=True, null=True)
    low_price_minmax_15 = models.FloatField(blank=True, null=True)
    low_price_minmax_20 = models.FloatField(blank=True, null=True)
    close_price_minmax_3 = models.FloatField(blank=True, null=True)
    close_price_minmax_5 = models.FloatField(blank=True, null=True)
    close_price_minmax_15 = models.FloatField(blank=True, null=True)
    close_price_minmax_20 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_volprice_1'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DVolprice2(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    cft_decay10 = models.FloatField(blank=True, null=True)
    cft_lh_cov10 = models.FloatField(blank=True, null=True)
    cft_vl_cov10 = models.FloatField(blank=True, null=True)
    cft_vwapc_cov10 = models.FloatField(blank=True, null=True)
    c_decay10 = models.FloatField(blank=True, null=True)
    c_lh_corr10 = models.FloatField(blank=True, null=True)
    c_lh_cov10 = models.FloatField(blank=True, null=True)
    c_ret10 = models.FloatField(blank=True, null=True)
    c_r_corr10 = models.FloatField(blank=True, null=True)
    c_std10 = models.FloatField(blank=True, null=True)
    c_vwap_cov10 = models.FloatField(blank=True, null=True)
    ft_lh_cov10 = models.FloatField(blank=True, null=True)
    ft_std10 = models.FloatField(blank=True, null=True)
    ft_vl_corr10 = models.FloatField(blank=True, null=True)
    ft_vl_cov10 = models.FloatField(blank=True, null=True)
    h_r_corr10 = models.FloatField(blank=True, null=True)
    h_vwapc_cov10 = models.FloatField(blank=True, null=True)
    h_vwaph_corr10 = models.FloatField(blank=True, null=True)
    h_vwaph_cov10 = models.FloatField(blank=True, null=True)
    lh_std10 = models.FloatField(blank=True, null=True)
    lh_vwapc_corr10 = models.FloatField(blank=True, null=True)
    lh_vwapc_cov10 = models.FloatField(blank=True, null=True)
    lh_zscore10 = models.FloatField(blank=True, null=True)
    l_vwaph_corr10 = models.FloatField(blank=True, null=True)
    l_vwaph_cov10 = models.FloatField(blank=True, null=True)
    o_lh_corr10 = models.FloatField(blank=True, null=True)
    o_r_cov10 = models.FloatField(blank=True, null=True)
    o_vwapc_cov10 = models.FloatField(blank=True, null=True)
    r_lh_corr10 = models.FloatField(blank=True, null=True)
    r_lh_cov10 = models.FloatField(blank=True, null=True)
    r_vl_cov10 = models.FloatField(blank=True, null=True)
    r_vwapc_corr10 = models.FloatField(blank=True, null=True)
    r_vwaph_cov10 = models.FloatField(blank=True, null=True)
    r_zscore10 = models.FloatField(blank=True, null=True)
    vl_decay10 = models.FloatField(blank=True, null=True)
    vl_lh_cov10 = models.FloatField(blank=True, null=True)
    v_decay10 = models.FloatField(blank=True, null=True)
    v_lh_cov10 = models.FloatField(blank=True, null=True)
    v_r_cov10 = models.FloatField(blank=True, null=True)
    vwapc_decay10 = models.FloatField(blank=True, null=True)
    vwapc_ret10 = models.FloatField(blank=True, null=True)
    vwaph_lh_cov10 = models.FloatField(blank=True, null=True)
    vwaph_std10 = models.FloatField(blank=True, null=True)
    vwap_ft_cov10 = models.FloatField(blank=True, null=True)
    vwap_ret10 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_volprice_2'
        unique_together = (('trading_date', 'type_name_ab'),)


class Fv1DVolprice3(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    mom5_10 = models.FloatField(blank=True, null=True)
    mom5_15 = models.FloatField(blank=True, null=True)
    mom10_20 = models.FloatField(blank=True, null=True)
    mom10_25 = models.FloatField(blank=True, null=True)
    mom15_30 = models.FloatField(blank=True, null=True)
    mom15_40 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_1d_volprice_3'
        unique_together = (('trading_date', 'type_name_ab'),)


class FvDTech1(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=50)
    next_1_dc = models.CharField(max_length=20, blank=True, null=True)
    next_2_dc = models.CharField(max_length=20, blank=True, null=True)
    atr = models.FloatField(blank=True, null=True)
    exp_mom1_1 = models.FloatField(blank=True, null=True)
    exp_mom1_2 = models.FloatField(blank=True, null=True)
    exp_mom1_3 = models.FloatField(blank=True, null=True)
    exp_mom2_1 = models.FloatField(blank=True, null=True)
    exp_mom2_2 = models.FloatField(blank=True, null=True)
    exp_mom2_3 = models.FloatField(blank=True, null=True)
    mom = models.FloatField(blank=True, null=True)
    roll_ret1 = models.FloatField(blank=True, null=True)
    roll_ret2 = models.FloatField(blank=True, null=True)
    roll_ret3 = models.FloatField(blank=True, null=True)
    roll_avg = models.FloatField(blank=True, null=True)
    roll = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_d_tech_1'
        unique_together = (('trading_date', 'type_name_ab'),)


class FvDVlmprc1(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=45)
    pre_oi = models.FloatField(blank=True, null=True)
    pre_volume = models.FloatField(blank=True, null=True)
    pre_amount = models.FloatField(blank=True, null=True)
    oi_pct_change = models.FloatField(blank=True, null=True)
    v_pct_change = models.FloatField(blank=True, null=True)
    m_pct_change = models.FloatField(blank=True, null=True)
    hl_diff = models.FloatField(blank=True, null=True)
    co_diff = models.FloatField(blank=True, null=True)
    vwap = models.FloatField(blank=True, null=True)
    preclose_2od = models.FloatField(blank=True, null=True)
    preclose_5od = models.FloatField(blank=True, null=True)
    preclose_10od = models.FloatField(blank=True, null=True)
    preclose_20od = models.FloatField(blank=True, null=True)
    return_1od = models.FloatField(blank=True, null=True)
    return_2od = models.FloatField(blank=True, null=True)
    return_5od = models.FloatField(blank=True, null=True)
    return_10od = models.FloatField(blank=True, null=True)
    return_20od = models.FloatField(blank=True, null=True)
    low_p_2od = models.FloatField(blank=True, null=True)
    low_p_5od = models.FloatField(blank=True, null=True)
    low_p_10od = models.FloatField(blank=True, null=True)
    low_p_20od = models.FloatField(blank=True, null=True)
    drawdown_1od = models.FloatField(blank=True, null=True)
    drawdown_2od = models.FloatField(blank=True, null=True)
    drawdown_5od = models.FloatField(blank=True, null=True)
    drawdown_10od = models.FloatField(blank=True, null=True)
    drawdown_20od = models.FloatField(blank=True, null=True)
    high_p_2od = models.FloatField(blank=True, null=True)
    high_p_5od = models.FloatField(blank=True, null=True)
    high_p_10od = models.FloatField(blank=True, null=True)
    high_p_20od = models.FloatField(blank=True, null=True)
    drawup_1od = models.FloatField(blank=True, null=True)
    drawup_2od = models.FloatField(blank=True, null=True)
    drawup_5od = models.FloatField(blank=True, null=True)
    drawup_10od = models.FloatField(blank=True, null=True)
    drawup_20od = models.FloatField(blank=True, null=True)
    vol_2od = models.FloatField(blank=True, null=True)
    vol_5od = models.FloatField(blank=True, null=True)
    vol_10od = models.FloatField(blank=True, null=True)
    vol_20od = models.FloatField(blank=True, null=True)
    return_voladj_1od = models.FloatField(blank=True, null=True)
    return_voladj_2od = models.FloatField(blank=True, null=True)
    return_voladj_5od = models.FloatField(blank=True, null=True)
    return_voladj_10od = models.FloatField(blank=True, null=True)
    return_voladj_20od = models.FloatField(blank=True, null=True)
    high_price_percentile_3 = models.FloatField(blank=True, null=True)
    high_price_percentile_5 = models.FloatField(blank=True, null=True)
    high_price_percentile_10 = models.FloatField(blank=True, null=True)
    high_price_percentile_15 = models.FloatField(blank=True, null=True)
    high_price_percentile_20 = models.FloatField(blank=True, null=True)
    low_price_percentile_3 = models.FloatField(blank=True, null=True)
    low_price_percentile_5 = models.FloatField(blank=True, null=True)
    low_price_percentile_10 = models.FloatField(blank=True, null=True)
    low_price_percentile_15 = models.FloatField(blank=True, null=True)
    low_price_percentile_20 = models.FloatField(blank=True, null=True)
    close_price_percentile_3 = models.FloatField(blank=True, null=True)
    close_price_percentile_5 = models.FloatField(blank=True, null=True)
    close_price_percentile_10 = models.FloatField(blank=True, null=True)
    close_price_percentile_15 = models.FloatField(blank=True, null=True)
    close_price_percentile_20 = models.FloatField(blank=True, null=True)
    volume_percentile_3 = models.FloatField(blank=True, null=True)
    volume_percentile_5 = models.FloatField(blank=True, null=True)
    volume_percentile_10 = models.FloatField(blank=True, null=True)
    volume_percentile_15 = models.FloatField(blank=True, null=True)
    volume_percentile_20 = models.FloatField(blank=True, null=True)
    amount_percentile_3 = models.FloatField(blank=True, null=True)
    amount_percentile_5 = models.FloatField(blank=True, null=True)
    amount_percentile_10 = models.FloatField(blank=True, null=True)
    amount_percentile_15 = models.FloatField(blank=True, null=True)
    amount_percentile_20 = models.FloatField(blank=True, null=True)
    oi_percentile_3 = models.FloatField(blank=True, null=True)
    oi_percentile_5 = models.FloatField(blank=True, null=True)
    oi_percentile_10 = models.FloatField(blank=True, null=True)
    oi_percentile_15 = models.FloatField(blank=True, null=True)
    oi_percentile_20 = models.FloatField(blank=True, null=True)
    high_price_minmax_3 = models.FloatField(blank=True, null=True)
    high_price_minmax_5 = models.FloatField(blank=True, null=True)
    high_price_minmax_10 = models.FloatField(blank=True, null=True)
    high_price_minmax_15 = models.FloatField(blank=True, null=True)
    high_price_minmax_20 = models.FloatField(blank=True, null=True)
    low_price_minmax_3 = models.FloatField(blank=True, null=True)
    low_price_minmax_5 = models.FloatField(blank=True, null=True)
    low_price_minmax_10 = models.FloatField(blank=True, null=True)
    low_price_minmax_15 = models.FloatField(blank=True, null=True)
    low_price_minmax_20 = models.FloatField(blank=True, null=True)
    close_price_minmax_3 = models.FloatField(blank=True, null=True)
    close_price_minmax_5 = models.FloatField(blank=True, null=True)
    close_price_minmax_10 = models.FloatField(blank=True, null=True)
    close_price_minmax_15 = models.FloatField(blank=True, null=True)
    close_price_minmax_20 = models.FloatField(blank=True, null=True)
    volume_minmax_3 = models.FloatField(blank=True, null=True)
    volume_minmax_5 = models.FloatField(blank=True, null=True)
    volume_minmax_10 = models.FloatField(blank=True, null=True)
    volume_minmax_15 = models.FloatField(blank=True, null=True)
    volume_minmax_20 = models.FloatField(blank=True, null=True)
    amount_minmax_3 = models.FloatField(blank=True, null=True)
    amount_minmax_5 = models.FloatField(blank=True, null=True)
    amount_minmax_10 = models.FloatField(blank=True, null=True)
    amount_minmax_15 = models.FloatField(blank=True, null=True)
    amount_minmax_20 = models.FloatField(blank=True, null=True)
    oi_minmax_3 = models.FloatField(blank=True, null=True)
    oi_minmax_5 = models.FloatField(blank=True, null=True)
    oi_minmax_10 = models.FloatField(blank=True, null=True)
    oi_minmax_15 = models.FloatField(blank=True, null=True)
    oi_minmax_20 = models.FloatField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fv_d_vlmprc_1'
        unique_together = (('trading_date', 'type_name_ab'),)


class FvFactorInfo(models.Model,BaseModel):
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
        db_table = 'fv_factor_info'
        unique_together = (('table_name', 'factor_name'),)
