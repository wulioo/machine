from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from extra.db.base_model import BaseModel


class SysMenu(models.Model):
    menu_id = models.BigAutoField(primary_key=True)
    # pid_id = models.BigIntegerField(blank=True, null=True)
    pid = models.ForeignKey("self", null=True, blank=True, related_name="children", on_delete=models.CASCADE,
                            db_constraint=False, default=0)
    platform = models.IntegerField(blank=True, null=True)

    sub_count = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    component = models.CharField(max_length=255, blank=True, null=True)
    menu_sort = models.IntegerField(blank=True, null=True)
    icon = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    i_frame = models.BooleanField(blank=True, null=True)
    cache = models.BooleanField(blank=True, null=True)
    hidden = models.BooleanField(blank=True, null=True)
    permission = models.CharField(max_length=255, blank=True, null=True)
    create_by = models.CharField(max_length=255, blank=True, null=True)
    update_by = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_menu'


class SysConf(models.Model, BaseModel):
    id = models.IntegerField(primary_key=True)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    remark = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sys_conf'
