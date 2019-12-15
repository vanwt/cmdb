from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from ..api import *

router = DefaultRouter()
router.register("user", UserApiView)
router.register("role", RoleViewSet)
router.register("permission", PermissionViewSet)
router.register("menu", MenuViewSet)

urlpatterns = [
    path("user/login/", obtain_jwt_token),
    path("user/logout/", LogoutApiView.as_view()),
    path("user/role/<str:key>/", UserChaneRole.as_view()),
    path("user/test/", Test.as_view()),

    path("role/permission/<str:id>/", RolePermission.as_view()),
    path("role/status/", ChangeRoleStatus.as_view()),
    path("role/menu/<str:id>/", RoleMenu.as_view()),

    path("permission/status/", ChangePermissionStatus.as_view())
]

urlpatterns += router.urls
