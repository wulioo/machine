# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.system.serializers import SystemMenuSerializer, SystemMenuLazySerializer, SystemMenuListSerializer
from apps.user.models import SysRole

User = get_user_model()


class LoginSerializer(TokenObtainPairSerializer):
    mobile = serializers.CharField(max_length=11)

    class Meta:
        model = User
        fields = "username"


class UserRolesSerializer(serializers.ModelSerializer):
    # meta = serializers.SerializerMethodField()
    dataScope = serializers.CharField(source='data_scope')
    updateBy = serializers.CharField(source='update_by')
    createTime = serializers.DateTimeField(source='create_time')
    menus = SystemMenuListSerializer(many=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = SysRole
        fields = ['dataScope', 'id', 'level', 'name', 'updateBy', 'description', 'createTime', 'menus','user']

    def get_user(self, obj):
        user_list = obj.role_set.all()

        return [user.id for user in user_list]

class UserRolesAddSerializer(serializers.ModelSerializer):
    dataScope = serializers.CharField(max_length=255, write_only=True)
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user_id_list = self.context['request'].data['user']
        user_list = obj.role_set.all()
        for user in user_list:
            obj.role_set.remove(user)
        query_user = User.objects.filter(id__in=user_id_list)
        for user in query_user:
            obj.role_set.add(user)
        return user_id_list
    class Meta:
        model = SysRole
        fields = ['dataScope', 'level', 'name', 'description',"user"]

    def create(self, validated_data):
        instance = SysRole.objects.create(
            data_scope=validated_data['dataScope'],
            level=validated_data['level'],
            name=validated_data['name'],
            description=validated_data['description'],
            create_time=datetime.now()
        )
        return instance


class UserRolesPutSerializer(serializers.ModelSerializer):
    menus = serializers.ListField()

    class Meta:
        model = SysRole
        fields = ['id', 'menus']

    def update(self, instance, validated_data):
        pass
        return instance
