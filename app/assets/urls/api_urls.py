from rest_framework.routers import DefaultRouter
from django.urls import path
from ..api import *

router = DefaultRouter()
# 只有查删
router.register("assets/info", AssetsInfoViewSet)
router.register("assets", AssetsViewSet)
router.register("idc", IDCViewSet)
router.register("tag", TagViewSet)

urlpatterns = [
    path("assets/test-connect/", TestConnectApiView.as_view()),
    path("assets/server-count/",ServerCount.as_view()),
    path("assets/vm-count/",VmCount.as_view())

]

urlpatterns += router.urls
