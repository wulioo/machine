from django.contrib import admin
from django.urls import path, re_path

from apps.equity.views import FactorCalEquityIcIr, FactorEqZonalTesting, FactorEqNdcg, FactorEqICIRReview, FactorEqZonalTestingReview, FactorEqNDCGReview, FactorEqDistribute, FactorEqCorr, \
    FactorEqBacktesting, FactorEqAvgVarie, FactorEqCorrReview, FactorEqDistributeReview, FactorEqBackTestIngReview

urlpatterns = [
    path('distribute/', FactorEqDistribute.as_view({'post': 'create'})),
    path('icir/', FactorCalEquityIcIr.as_view({'post': 'create'})),
    path('zonaltesting/', FactorEqZonalTesting.as_view({'post': 'create'})),
    path('ndcg/', FactorEqNdcg.as_view({'post': 'create'})),
    path('corr/', FactorEqCorr.as_view({'post': 'create'})),
    path('backtesting/', FactorEqBacktesting.as_view({'post': 'create'})),
    path('varie/avg/', FactorEqAvgVarie.as_view({'post': 'create'})),
    path('review/icir', FactorEqICIRReview.as_view({'post': 'create'})),
    path('review/layered', FactorEqZonalTestingReview.as_view({'post': 'create'})),
    path('review/distribute/', FactorEqDistributeReview.as_view({'post': 'create'})),
    path('review/backtesting/', FactorEqBackTestIngReview.as_view({'post': 'create'})),
    path('review/ndcg', FactorEqNDCGReview.as_view({'post': 'create'})),
    path('review/corr', FactorEqCorrReview.as_view({'post': 'create'})),
]
