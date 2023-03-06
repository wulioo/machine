from django.contrib import admin
from django.urls import path

from apps.api_fv_section.views import FactorApiList, FvScCalRankICIR

urlpatterns = [

    path('rank/ic', FvScCalRankICIR.as_view({'post': 'create'})),
    path('factor/list', FactorApiList.as_view()),

]
