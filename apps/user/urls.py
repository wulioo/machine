from django.contrib import admin
from django.urls import path, re_path

from apps.system.views import SystemConfigList
from apps.user.views import LoginView, UserRolesList, UserRolesLevel, UserRolesMenu

urlpatterns = [
    # path(r'login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', LoginView.as_view()),
    # re_path('roles/(?P<pk>\d+)/$', UserRolesList.as_view({, })),

    path('roles/', UserRolesList.as_view({'get': 'list', 'post': 'create'})),
    # re_path('roles/(?P<pk>\d+)/$', UserRolesList.as_view({'delete': 'destroy', 'put': 'update'})),
    re_path('roles/(?P<pk>\d+)/$', UserRolesList.as_view({'delete': 'destroy', 'put': 'update','get': 'retrieve'})),

    # re_path('menus/(?P<menu_id>\d+)/$', SystemMenusList.as_view({'delete': 'destroy', 'put': 'update'})),
    re_path('roles/menu/', UserRolesMenu.as_view({'post': 'create'})),
    path('roles/level/', UserRolesLevel.as_view({'get': 'list'}))

]
