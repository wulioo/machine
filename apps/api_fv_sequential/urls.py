from django.contrib import admin
from django.urls import path

from apps.api_fv_section.views import FactorApiList
from apps.api_fv_sequential.views import FvSqCalIC, FvSqApiList, FvSqCalRankICIR

urlpatterns = [
    path('ic', FvSqCalIC.as_view({'post': 'create'})),
    path('rank/ic', FvSqCalRankICIR.as_view({'post': 'create'})),
    path('type/list', FvSqApiList.as_view()),

]
