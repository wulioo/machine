from django.contrib import admin
from django.urls import path
from apps.future.views import FactorList, FvCalICIR, FactorZonalTesting, FactorIcByRedis, \
    FactorEchartsByRedis, FactorICIRReview, FactorNDCGReview, FactorZonalTestingReview, \
    FutureFactorCorr, FactorCorrReview, FactorCorrByRedis, FactorCategoryList, \
    FactorCalEarnings, FactorCalSharpeEarnings, FvFactorAvgVarie, \
    FutureFactorDistribute, FvFactorReviewDistribute, FactorFvPositioning, FactorFvBacktesting, FvFactorBacktestingByRedis, \
    FvFactorBackTestIngReview, FactorFvNdcg, FactorFvAvgVarie, GetMysqlData

urlpatterns = [
    path('list/', FactorList.as_view()),
    path('category/list/', FactorCategoryList.as_view()),
    path('ic/', FactorIcByRedis.as_view({'post': 'create'})),
    path('getcorr/', FactorCorrByRedis.as_view({'post': 'create'})),
    path('icir/', FvCalICIR.as_view({'post': 'create'})),
    path('ndcg/', FactorFvNdcg.as_view({'post': 'create'})),
    path('corr/', FutureFactorCorr.as_view({'post': 'create'})),
    path('review/icir', FactorICIRReview.as_view({'post': 'create'})),
    path('review/ndcg', FactorNDCGReview.as_view({'post': 'create'})),
    path('review/layered', FactorZonalTestingReview.as_view({'post': 'create'})),
    path('review/corr', FactorCorrReview.as_view({'post': 'create'})),
    path('zonaltesting/', FactorZonalTesting.as_view({'post': 'create'})),
    path('earnings/n/', FactorCalEarnings.as_view({'post': 'create'})),
    path('earnings/sharpe/', FactorCalSharpeEarnings.as_view({'post': 'create'})),
    path('echarts/', FactorEchartsByRedis.as_view({'post': 'create'})),

    path('varie/avg/', FactorFvAvgVarie.as_view({'post': 'create'})),
    path('distribute/', FutureFactorDistribute.as_view({'post': 'create'})),
    path('review/distribute/', FvFactorReviewDistribute.as_view({'post': 'create'})),
    path('positioning/', FactorFvPositioning.as_view({'post': 'create'})),
    path('backtesting/', FactorFvBacktesting.as_view({'post': 'create'})),
    path('review/backtesting/', FvFactorBackTestIngReview.as_view({'post': 'create'})),
    path('backtesting/echarts', FvFactorBacktestingByRedis.as_view({'post': 'create'})),
    path('read/sql/', GetMysqlData.as_view()),
]
