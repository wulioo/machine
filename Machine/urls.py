"""Machine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # 导入 factor子应用的路由
    path('future/', include('apps.future.urls')),
    path('equity/', include('apps.equity.urls')),
    #系统
    path('system/', include('apps.system.urls')),
    # 身份认证
    path('auth/', include('apps.user.urls')),
    # 钩子函数
    path('hook/', include('apps.hook.urls')),
    # 监控程序
    path('fv/cm/', include('apps.monitor.urls')),
    # 时序因子路由
    path('fv/sq/', include('apps.fv_sequential.urls')),
    # 期货因子截面api
    path('api/fv/sc/', include('apps.api_fv_section.urls')),
    # 期货因子时序api
    path('api/fv/sq/', include('apps.api_fv_sequential.urls')),
]
