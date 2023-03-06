# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from apps.system.models import SysMenu


class SysRole(models.Model):
    # role_id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(unique=True, max_length=255)
    level = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    data_scope = models.CharField(max_length=255, blank=True, null=True)
    create_by = models.CharField(max_length=255, blank=True, null=True)
    update_by = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    menus = models.ManyToManyField(
        SysMenu,
        verbose_name='拥有所有的菜单',
        blank=True,
        related_name="menu_set",
        related_query_name="menu",
        db_constraint=False
    )

    class Meta:
        # managed = False
        db_table = 'sys_role'



class User(AbstractUser):
    """
    用户
    """
    nick_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    # birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    avatar_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="头像地址")
    avatar_path = models.CharField(null=True, blank=True, max_length=255, verbose_name="头像真实路径")
    create_time = models.DateField(blank=True, null=True, auto_now_add=True)
    update_time = models.DateField(blank=True, null=True, auto_now_add=True)
    groups = models.ManyToManyField(
        SysRole,
        verbose_name='拥有的所有角色',
        blank=True,
        related_name="role_set",
        related_query_name="role",
        db_constraint=False,
    )

    # roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='SysRole', blank=True)

    class Meta:
        # managed = False
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        db_table = 'sys_user'

    def __str__(self):
        return self.username
