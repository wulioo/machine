from django.contrib import admin
from django.urls import path, re_path

from apps.hook.views import HookDeployment
from apps.system.views import SystemConfigList
from apps.user.views import LoginView, UserRolesList, UserRolesLevel, UserRolesMenu

urlpatterns = [
    path('git/deployment/', HookDeployment.as_view()),


]
