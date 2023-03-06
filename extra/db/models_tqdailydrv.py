from django.db import models
from extra.db.base_model import BaseModel


class DwsTradingTimeFutureDaily(models.Model, BaseModel):
    trading_date = models.DateField(primary_key=True)
    type_name_ab = models.CharField(max_length=20)
    trading_time_list = models.JSONField(blank=True, null=True)
    upload_user = models.CharField(max_length=50)
    upload_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dws_trading_time_future_daily'
        unique_together = (('trading_date', 'type_name_ab'),)
