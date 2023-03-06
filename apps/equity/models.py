from django.db import models

from extra.db.base_model import BaseModel


# Create your models here.

class EquityDailyType(models.Model,BaseModel):
    trading_date = models.DateField()
    index_code = models.CharField(max_length=255)
    total = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'equity_daily_type'

