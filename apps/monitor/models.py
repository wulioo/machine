import json

from django.db import models

from extra.db.base_model import BaseModel


# Create your models here.
class CmSecIcIr(models.Model, BaseModel):
    table = models.CharField(max_length=255)
    factor = models.CharField(max_length=255)
    rank_ic = models.FloatField()
    rank_ir = models.FloatField()
    label = models.CharField(max_length=255)
    status = models.IntegerField(choices=[(1, "selected"), (0, "not-selected")])
    is_night = models.IntegerField()
    remark = models.CharField(max_length=255)
    update_time = models.DateTimeField()
    create_time = models.DateTimeField()
    database = models.CharField(max_length=255, db_collation='utf8mb4_bin')

    class Meta:
        managed = False
        db_table = 'cm_sec_ic_ir'


class CmSeqIcIr(models.Model):
    type_name_ab = models.CharField(max_length=255)
    table = models.CharField(max_length=255)
    factor = models.CharField(max_length=255)
    rank_ic = models.FloatField()
    rank_ir = models.FloatField()
    windows = models.IntegerField()
    status = models.IntegerField(choices=[(1, "selected"), (0, "not-selected")])
    remark = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    update_time = models.DateTimeField()
    create_time = models.DateTimeField()
    database = models.CharField(max_length=255, db_collation='utf8mb4_bin')


    class Meta:
        managed = False
        db_table = 'cm_seq_ic_ir'





