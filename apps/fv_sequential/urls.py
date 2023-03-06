from django.contrib import admin
from django.urls import path

from apps.fv_sequential.views import FvCalIcIr, FvRedisIcIr, FvICIRReview, FvCalCorr

urlpatterns = [
    path('icir/', FvCalIcIr.as_view({'post': 'create'})),
    path('corr/', FvCalCorr.as_view({'post': 'create'})),
    path('review/icir/', FvICIRReview.as_view({'post': 'create'})),
    path('redis_icir/', FvRedisIcIr.as_view({'post': 'create'})),


]
