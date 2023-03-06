# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from extra.db.base_model import BaseModel


class SysTable(models.Model, BaseModel):
    tb_name = models.CharField(max_length=255, db_collation='utf8_general_ci')
    tb_note = models.CharField(max_length=255, db_collation='utf8_general_ci')
    database = models.CharField(max_length=100, db_collation='utf8_general_ci')
    tb_type = models.IntegerField()
    create_time = models.DateField(blank=True, null=True)
    update_time = models.DateField(blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sys_table'


class FutureDailyType(models.Model):
    trading_date = models.DateField()
    exchange = models.CharField(max_length=255)
    total = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'future_daily_type'
