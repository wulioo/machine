from django.contrib import admin
from django.urls import path, re_path

from apps.hook.views import HookDeployment
from apps.monitor.views import MonitorSecICIR, CmSecICIR, MonitorSeqICIR, CmSeqICIR, TypeNameAbList
from apps.system.views import SystemConfigList
from apps.user.views import LoginView, UserRolesList, UserRolesLevel, UserRolesMenu

urlpatterns = [
    path('sec/icir/', MonitorSecICIR.as_view()),
    path('seq/icir/', MonitorSeqICIR.as_view()),
    path('seq/type/list/', TypeNameAbList.as_view()),
    path('sec/icir/list/', CmSecICIR.as_view({'get': 'list'})),
    path('seq/icir/list/', CmSeqICIR.as_view({'get': 'list'})),
]
