from extra.db.base_model import BaseModel# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class EquityDaily(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    wind_code = models.CharField(max_length=10)
    pre_close = models.FloatField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.FloatField(blank=True, null=True)
    close_price = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    deal_number = models.FloatField(blank=True, null=True)
    change = models.FloatField(blank=True, null=True)
    pct_change = models.FloatField(blank=True, null=True)
    swing = models.FloatField(blank=True, null=True)
    vwap = models.FloatField(blank=True, null=True)
    adj_factor = models.FloatField(blank=True, null=True)
    turn = models.FloatField(blank=True, null=True)
    free_turn = models.FloatField(blank=True, null=True)
    last_tradeday = models.DateField(blank=True, null=True)
    last_tradeday_mkt = models.DateField(blank=True, null=True)
    is_st = models.IntegerField(db_column='is_ST', blank=True, null=True)  # Field name made lowercase.
    trade_status = models.CharField(max_length=10, blank=True, null=True)
    susp_days = models.IntegerField(blank=True, null=True)
    susp_reason = models.CharField(max_length=50, blank=True, null=True)
    max_up_or_down = models.IntegerField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'equity_daily'
        unique_together = (('trading_date', 'wind_code'),)


class EquityHeader(models.Model,BaseModel):
    wind_code = models.CharField(primary_key=True, max_length=9)
    trade_code = models.CharField(max_length=6)
    isin_code = models.CharField(max_length=12, blank=True, null=True)
    stock_name = models.CharField(max_length=50)
    stock_name_en = models.CharField(max_length=100, blank=True, null=True)
    hshare_windcode = models.CharField(max_length=10, blank=True, null=True)
    bshare_windcode = models.CharField(max_length=9, blank=True, null=True)
    bshare_code = models.CharField(max_length=6, blank=True, null=True)
    bshare_name = models.CharField(max_length=50, blank=True, null=True)
    ipo_date = models.DateField()
    exchange_cn = models.CharField(max_length=20)
    exchange_en = models.CharField(max_length=10)
    mkt = models.CharField(max_length=10)
    stock_status = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)
    par_value = models.CharField(max_length=20)
    lot_size = models.IntegerField(blank=True, null=True)
    trading_unit = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=6)
    pre_name = models.CharField(max_length=255, blank=True, null=True)
    exch_city = models.CharField(max_length=10)
    stock_class = models.CharField(max_length=50)
    security_type = models.CharField(max_length=10)
    is_backdoor = models.CharField(max_length=1, blank=True, null=True)
    backdoor_date = models.DateField(blank=True, null=True)
    delist_date = models.DateField(blank=True, null=True)
    found_date = models.DateField(blank=True, null=True)
    province = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'equity_header'
        unique_together = (('wind_code', 'upload_time'),)


class EtfHeader(models.Model,BaseModel):
    wind_code = models.CharField(max_length=9)
    trade_code = models.CharField(max_length=6)
    isin_code = models.CharField(max_length=12, blank=True, null=True)
    stock_name = models.CharField(max_length=50)
    stock_name_en = models.CharField(max_length=100, blank=True, null=True)
    ipo_date = models.DateField()
    fund_setupdate = models.DateField()
    exchange_cn = models.CharField(max_length=20)
    exchange_en = models.CharField(max_length=10)
    mkt = models.CharField(max_length=10)
    stock_status = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)
    country = models.CharField(max_length=6)
    pre_name = models.CharField(max_length=255, blank=True, null=True)
    exch_city = models.CharField(max_length=10)
    stock_class = models.CharField(max_length=5)
    security_type = models.CharField(max_length=10)
    delist_date = models.DateField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()
    track_indexcode = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'etf_header'


class FutureDaily(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    wind_code = models.CharField(max_length=20)
    pre_close = models.FloatField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.FloatField(blank=True, null=True)
    close_price = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    deal_number = models.FloatField(blank=True, null=True)
    net_change = models.FloatField(blank=True, null=True)
    pct_change = models.FloatField(blank=True, null=True)
    swing = models.FloatField(blank=True, null=True)
    vwap = models.FloatField(blank=True, null=True)
    open_interest = models.FloatField(blank=True, null=True)
    open_interest_chg = models.FloatField(blank=True, null=True)
    pre_settle = models.FloatField(blank=True, null=True)
    settle = models.FloatField(blank=True, null=True)
    long_margin = models.FloatField(blank=True, null=True)
    short_margin = models.FloatField(blank=True, null=True)
    st_stock = models.FloatField(blank=True, null=True)
    if_basis = models.FloatField(blank=True, null=True)
    tbf_ctd = models.CharField(db_column='tbf_CTD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    change_limit = models.FloatField(blank=True, null=True)
    is_dominant = models.IntegerField(blank=True, null=True)
    is_dominant_volume = models.IntegerField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'future_daily'
        unique_together = (('trading_date', 'wind_code'),)


class FutureDominantDaily(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=50)
    wind_code = models.CharField(max_length=50)
    last_tradedate = models.DateField()
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'future_dominant_daily'
        unique_together = (('trading_date', 'type_name_ab'),)


class FutureHeader(models.Model,BaseModel):
    wind_code = models.CharField(primary_key=True, max_length=20)
    type_name_ab = models.CharField(max_length=45, blank=True, null=True)
    ctp_code = models.CharField(max_length=20, blank=True, null=True)
    sec_name = models.CharField(max_length=25)
    sc_name = models.CharField(max_length=45, blank=True, null=True)
    sec_type = models.CharField(max_length=45, blank=True, null=True)
    ipo_date = models.DateField()
    last_tradedate = models.DateField()
    exchange_cn = models.CharField(max_length=20)
    exchange_en = models.CharField(max_length=10)
    currency = models.CharField(max_length=3)
    tunit = models.CharField(max_length=20)
    country = models.CharField(max_length=6)
    exchange_city = models.CharField(max_length=20)
    last_deliverydate = models.DateField()
    delivery_month = models.CharField(max_length=6)
    lprice = models.FloatField(blank=True, null=True)
    punit = models.CharField(max_length=20)
    mf_price = models.FloatField()
    contract_issuedate = models.DateField()
    contract_multiplier = models.FloatField()
    cdmonths = models.CharField(max_length=50)
    trading_hours = models.CharField(max_length=255)
    ltdated = models.CharField(max_length=200)
    ddate = models.CharField(max_length=100)
    ftmargins = models.CharField(max_length=50)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'future_header'


class IndexComponent(models.Model,BaseModel):
    trading_date = models.DateField(primary_key=True)
    wind_code = models.CharField(max_length=20)
    index_code = models.CharField(max_length=20)
    weight = models.FloatField()
    weight_tq = models.FloatField(blank=True, null=True)
    publish_date = models.DateField()
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'index_component'
        unique_together = (('trading_date', 'index_code', 'wind_code'),)


class OptionHeader(models.Model,BaseModel):
    wind_code = models.CharField(primary_key=True, max_length=20)
    ctp_code = models.CharField(max_length=20, blank=True, null=True)
    us_code = models.CharField(max_length=12)
    option_name = models.CharField(max_length=255)
    mf_price = models.FloatField(blank=True, null=True)
    exercise_type = models.CharField(max_length=6, blank=True, null=True)
    exe_price = models.FloatField(blank=True, null=True)
    exe_ratio = models.IntegerField(blank=True, null=True)
    total_duration = models.SmallIntegerField(blank=True, null=True)
    exercise_month = models.CharField(max_length=7)
    call_or_put = models.CharField(max_length=4)
    first_tradedate = models.DateField()
    last_tradedate = models.DateField()
    settle_method = models.CharField(max_length=10)
    exchange_cn = models.CharField(max_length=20)
    exchange_en = models.CharField(max_length=10)
    currency = models.CharField(max_length=3, blank=True, null=True)
    country = models.CharField(max_length=6)
    exchange_city = models.CharField(max_length=20)
    upload_user = models.CharField(max_length=20)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'option_header'


class TradingDateInfo(models.Model,BaseModel):
    nature_date = models.DateField(primary_key=True)
    exchange_cn = models.CharField(max_length=255)
    is_trading_date = models.TextField()  # This field type is a guess.
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'trading_date_info'
        unique_together = (('nature_date', 'exchange_cn'),)
