from datetime import datetime

import pandas as pd
from rest_framework import serializers

from apps.system.models import SysMenu


class SystemMenuSerializer3(serializers.ModelSerializer):
    meta = serializers.SerializerMethodField()

    class Meta:
        model = SysMenu
        fields = ['children', 'component', 'hidden', 'meta', 'name', 'path', 'platform']

    def get_meta(self, row):
        return {'icon': row.icon, 'noCache': row.cache, 'title': row.title}


class SystemMenuSerializer2(serializers.ModelSerializer):
    children = SystemMenuSerializer3(many=True)
    meta = serializers.SerializerMethodField()

    class Meta:
        model = SysMenu
        fields = ['children', 'component', 'hidden', 'meta', 'name', 'path', 'platform','menu_sort','menu_id']

    def get_meta(self, row):
        return {'icon': row.icon, 'noCache': row.cache, 'title': row.title}


class SystemMenuSerializer(serializers.ModelSerializer):
    alwaysShow = serializers.SerializerMethodField()
    # children = SystemMenuSerializer2(many=True)
    children = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    redirect = serializers.SerializerMethodField()

    class Meta:
        model = SysMenu
        fields = ['alwaysShow', 'children', 'component', 'hidden', 'meta', 'name', 'path', 'redirect', 'platform']

    def get_meta(self, row):
        return {'icon': row.icon, 'noCache': row.cache, 'title': row.title}

    def get_redirect(self, row):
        if row.pid_id == None:
            return 'noredirect'

    def get_alwaysShow(self, row):
        if row.pid_id == None:
            return True

    def get_children(self, row):
    
        groups = self.context['request'].user.groups.all()
        r_menu_id = []
        for role in groups:
            role_menu_df = pd.DataFrame(role.menus.all().values('menu_id'))
            if not role_menu_df.empty:
                r_menu_id += list(pd.DataFrame(role.menus.all().values('menu_id'))['menu_id'])
        res = SystemMenuSerializer2(row.children, many=True)
        platform = self.context['request'].query_params['platform']
        data = [val for val in res.data if val['platform'] in [int(platform), 0] and val['menu_id'] in set(r_menu_id)]

        return sorted(data, key=lambda r: r['menu_sort'])


class SystemMenuListSerializer(serializers.ModelSerializer):
    hasChildren = serializers.SerializerMethodField()
    id = serializers.IntegerField(source='menu_id')
    label = serializers.CharField(source='title')
    menuSort = serializers.IntegerField(source='menu_sort')
    subCount = serializers.IntegerField(source='sub_count')
    createTime = serializers.DateTimeField(source='create_time')
    iFrame = serializers.BooleanField(source='i_frame')
    componentName = serializers.CharField(source='name')

    class Meta:
        model = SysMenu
        fields = ['cache', 'createTime', 'hasChildren', 'hidden', 'iFrame', 'icon', 'id', 'label', 'menuSort',
                  'path', 'subCount', 'title', 'type', 'component', 'componentName', 'pid','platform']

    def get_hasChildren(self, row):
        if row.pid_id != None:
            return False
        return True


class SystemMenuLazySerializer3(SystemMenuListSerializer):
    pid = serializers.IntegerField(source='pid_id')

    class Meta:
        model = SysMenu
        fields = ['cache', 'createTime', 'hasChildren', 'hidden', 'iFrame', 'icon', 'id', 'label', 'menuSort',
                  'path', 'subCount', 'title', 'type', 'pid', 'componentName', 'component']


class SystemMenuLazySerializer2(SystemMenuListSerializer):
    pid = serializers.IntegerField(source='pid_id')
    children = SystemMenuLazySerializer3(many=True)

    class Meta:
        model = SysMenu
        fields = ['cache', 'createTime', 'hasChildren', 'hidden', 'iFrame', 'icon', 'id', 'label', 'menuSort',
                  'path', 'subCount', 'title', 'type', 'pid', 'componentName', 'component', 'children']


class SystemMenuLazySerializer(SystemMenuListSerializer):
    pid = serializers.IntegerField(source='pid_id')
    children = SystemMenuLazySerializer2(many=True)
    leaf = serializers.SerializerMethodField()

    class Meta:
        model = SysMenu
        fields = ['cache', 'createTime', 'hasChildren', 'hidden', 'iFrame', 'icon', 'id', 'label', 'menuSort',
                  'path', 'subCount', 'title', 'type', 'pid', 'componentName', 'component', 'children', 'leaf']

    def get_hasChildren(self, row):
        if row.pid_id != None:
            return False
        return True

    def get_leaf(self, row):
        return False


class SystemMenuPostSerializer(serializers.ModelSerializer):
    iFrame = serializers.BooleanField(required=True, write_only=True)
    componentName = serializers.CharField(required=False, max_length=50, write_only=True, allow_null=True)
    menuSort = serializers.IntegerField(write_only=True)
    pid = serializers.IntegerField(write_only=True, default=None)

    class Meta:
        model = SysMenu

        fields = ['cache', 'component', 'componentName', 'hidden', 'iFrame', 'icon', 'menuSort',
                  'path', 'permission', 'pid', 'title', 'type','platform']

    def create(self, validated_data):
        if validated_data['pid'] == 0:
            validated_data['pid'] = None
        instance = SysMenu.objects.create(
            cache=validated_data['cache'],
            component=validated_data['component'],
            name=validated_data['componentName'],
            hidden=validated_data['hidden'],
            i_frame=validated_data['iFrame'],
            icon=validated_data['icon'],
            menu_sort=validated_data['menuSort'],
            path=validated_data['path'],
            permission=validated_data['permission'],
            pid_id=validated_data['pid'],
            title=validated_data['title'],
            type=validated_data['type'],
            platform=validated_data['platform'],
            create_time=datetime.now()
        )

        return instance

    def update(self, instance, validated_data):
        if validated_data['pid'] == 0:
            validated_data['pid'] = None
        instance.name = validated_data['componentName']
        instance.cache = validated_data['cache']
        instance.component = validated_data['component']
        instance.hidden = validated_data['hidden']
        instance.i_frame = validated_data['iFrame']
        instance.icon = validated_data['icon']
        instance.menu_sort = validated_data['menuSort']
        instance.path = validated_data['path']
        instance.permission = validated_data['permission']
        instance.pid_id = validated_data['pid']
        instance.title = validated_data['title']
        instance.type = validated_data['type']
        instance.platform = validated_data['platform']
        instance.save()
        return instance
