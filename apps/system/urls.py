from django.contrib import admin
from django.urls import path, re_path

from apps.system.views import SystemConfigList, SystemMenusBuild, SystemMenusList, SystemMenusLazy, SystemMenusChild, \
    SystemModel, SystemVersion

urlpatterns = [
    path('config/', SystemConfigList.as_view()),
    path('restart/django', SystemModel.as_view()),
    path('version/', SystemVersion.as_view()),
    path('menus/build/', SystemMenusBuild.as_view({'get': 'list'})),
    path('menus/lazy/', SystemMenusLazy.as_view({'get': 'list'})),
    re_path('menus/(?P<menu_id>\d+)/$', SystemMenusList.as_view({'delete': 'destroy', 'put': 'update'})),

    path('menus/', SystemMenusList.as_view({'get': 'list', 'post': 'create'})),
    path('menus/superior/', SystemMenusLazy.as_view({'get': 'list'})),
    re_path('menus/child/(?P<menu_id>\d+)/$', SystemMenusChild.as_view({'get': 'retrieve'}))

]
