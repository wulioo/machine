import datetime
import os
import platform
import time

import pandas as pd
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.views import APIView
import psutil
from rest_framework.response import Response

from Machine.settings import BASE_DIR
from apps.future.models import SysTable
from apps.system.filter import SysMenuFilter
from apps.system.models import SysMenu, SysConf
from apps.system.serializers import SystemMenuSerializer, SystemMenuListSerializer, SystemMenuLazySerializer, \
    SystemMenuPostSerializer
from apps.system.tasks import celery_restart_django
from apps.user.models import User, SysRole
from logs import logger
from utils.config import SYS_VERSION


class SystemConfigList(APIView):
    def get(self, request, *args, **kwargs):
        result = {
            'cpu': {},
            'memory': {},
            "swap": {},
            'disk': {},
            'sys': {}

        }
        mem = psutil.virtual_memory()
        smem = psutil.swap_memory()
        diskuse = psutil.disk_usage('/')

        # cpuinfo = wmi.WMI()

        result['sys']['os'] = platform.platform()
        result['sys']['day'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time()))
        try:
            result['sys']['ip'] = psutil.net_if_addrs()['eno1'][0].address
        except Exception as e:
            pass

        result['memory']['total'] = str(int(mem.total / (1024.0 * 1024.0 * 1024.0))) + "G"
        # 系统已经使用内存
        result['memory']['used'] = str(int(mem.used / (1024.0 * 1024.0 * 1024.0))) + "G"
        # 系统可用内存
        result['memory']['available'] = str(int(mem.available / (1024.0 * 1024.0 * 1024.0))) + " G"
        # 系统内存百分比
        result['memory']['usageRate'] = str(int(mem.percent))

        # 系统交换区内存
        result['swap']['total'] = str(float(smem.total / (1024.0 * 1024.0 * 1024.0))) + "G"
        result['swap']['used'] = str(int(smem.used / (1024.0 * 1024.0 * 1024.0))) + "G"
        result['swap']['available'] = str(int(smem.free / (1024.0 * 1024.0 * 1024.0))) + "G"
        result['swap']['usageRate'] = str(int(smem.percent))

        # cpu
        result['cpu']['core'] = f"{psutil.cpu_count()}个物理核心"
        result['cpu']['logic'] = f"{psutil.cpu_count(logical=False)}个逻辑核心"
        result['cpu']['used'] = psutil.cpu_percent()
        result['cpu']['idle'] = 100 - psutil.cpu_percent()
        # result['cpu']['name'] = cpuinfo.Win32_Processor()[0].Name
        # result['cpu']['package'] = f"{len(cpuinfo.Win32_Processor())}个物理CPU"

        # disk
        result['disk']['total'] = str(int(diskuse.total / (1024.0 * 1024.0 * 1024.0))) + "G"
        result['disk']['used'] = str(int(diskuse.used / (1024.0 * 1024.0 * 1024.0))) + "G"
        result['disk']['available'] = str(int(diskuse.free / (1024.0 * 1024.0 * 1024.0))) + "G"
        result['disk']['usageRate'] = str(int(diskuse.percent))
        result['time'] = datetime.datetime.now().strftime('%H:%M:%S')

        return Response(result)


class SystemModel(APIView):
    def get(self, request, *args, **kwargs):
        tq_list = ['tq_factor', 'tqmain']
        for val in tq_list:
            if val == 'tq_factor':
                factor_file_path = f'{BASE_DIR}/extra/db/models_tqfactor.py'
            elif val == 'tqmain':
                factor_file_path = f'{BASE_DIR}/extra/db/models_tqmain.py'
            else:
                factor_file_path = None

            os.system(f'python3 {BASE_DIR}/manage.py inspectdb --database {val} > {factor_file_path}')
            with open(f'{factor_file_path}', 'r') as f:
                file_content = f.read().replace('(models.Model)', '(models.Model,BaseModel)')
                if val == 'tq_factor':
                    file_content = file_content.replace('lrsr_top20_ma_5', 'LRSR_top20_ma_5')
                    file_content = file_content.replace('cpv_20', 'CPV_20')
                    file_content = file_content.replace('cpv_60', 'CPV_60')
                    file_content = file_content.replace('cpv_120', 'CPV_120')
                    file_content = file_content.replace('rcpv_5_10_60', 'RCPV_5_10_60')
                    file_content = file_content.replace('rcpv_5_20_60', 'RCPV_5_20_60')
                    file_content = file_content.replace('rcpv_5_30_60', 'RCPV_5_30_60')
                    file_content = file_content.replace('rcpv_10_10_60', 'RCPV_10_10_60')
                    file_content = file_content.replace('rcpv_10_20_60', 'RCPV_10_20_60')
                    file_content = file_content.replace('rcpv_10_30_60', 'RCPV_10_30_60')
                file_content = file_content.replace('[0m', '')

            with open(f'{factor_file_path}', 'w') as f:
                f.write('from extra.db.base_model import BaseModel')
                f.write(file_content)

        # 获取本地时间
        ctime = datetime.datetime.now()
        utc_ctime = datetime.datetime.utcfromtimestamp(ctime.timestamp())
        target_time = utc_ctime + datetime.timedelta(seconds=10)
        result = celery_restart_django.apply_async(args=[], eta=target_time)
        return Response(result.id)


class SystemVersion(APIView):

    def get(self, request, *args, **kwargs):
        conf = SysConf.get_info_all(Q(model='system'), ['key', 'value'])
        version = conf.loc[conf['key'] == "SYS_VERSION",'value'].iloc[0]
        return Response(version)


class SystemMenusBuild(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SysMenu.objects.filter(Q(hidden=False) & Q(type=0)).all().order_by('menu_sort')
    serializer_class = SystemMenuSerializer

    def get_queryset(self):
        groups = self.request.user.groups.all()
        r_menu_id = []
        for role in groups:
            role_menu_df = pd.DataFrame(role.menus.all().values('menu_id'))
            if not role_menu_df.empty:
                r_menu_id += list(pd.DataFrame(role.menus.all().values('menu_id'))['menu_id'])
        return SysMenu.objects.filter(Q(hidden=False) & Q(type=0) & Q(menu_id__in=set(r_menu_id))).all().order_by('menu_sort')

    # 过滤、搜索、排序
    # 这里的filter_backends指定了过滤的类型，此处设定了DjangoFilterBackend（过滤）、

    # filter_backends = (DjangoFilterBackend, )
    # filterset_fields = ('platform',)
    # filterset_class = SysMenuFilter


class SystemMenusList(viewsets.ModelViewSet):
    serializer_class = SystemMenuListSerializer
    lookup_field = 'menu_id'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'content': serializer.data, 'totalElements': len(serializer.data)})

    def get_queryset(self):

        if self.action == 'destroy' or self.action == 'update':
            return SysMenu.objects.all().order_by('menu_sort')
        else:
            pid = self.request.query_params.get('pid')
            if not pid:
                return SysMenu.objects.filter(Q(type=0)).all().order_by('menu_sort')

            return SysMenu.objects.filter(pid_id=pid).all().order_by('menu_sort')

    def get_serializer_class(self):
        if self.action == 'list':
            return SystemMenuListSerializer
        elif self.action == 'create' or self.action == 'update':
            return SystemMenuPostSerializer


class SystemMenusLazy(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SystemMenuLazySerializer

    def get_queryset(self):
        pid = self.request.query_params.get('pid')
        if not pid or int(pid) == 0:
            return SysMenu.objects.filter(type=0).all()

        return SysMenu.objects.filter(pid_id=pid).all()


class SystemMenusChild(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = SysMenu.objects.all()
    serializer_class = SystemMenuLazySerializer
    lookup_field = 'menu_id'
    data = []

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        new_arr = []

        data = self.responce(serializer.data, new_arr)
        return Response(data)

    def responce(self, data, new_arr):
        new_arr.append(data['id'])
        if data['children']:
            for val_child in data['children']:
                self.responce(val_child, new_arr)
        return new_arr
