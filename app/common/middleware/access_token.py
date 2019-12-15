from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.http import HttpResponseForbidden, HttpResponseNotFound
from user.models import UrlPermission
import json


class AccessControlMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        目前想法是
        1. 先检查是否登录,若未登录且url在未登录角色的允许访问Url中,可访问
        2. 检查是否登录，若未登录 跳转到登录页
        3. 检测 登录用户是否是 超级用户,若是可访问
        4. 遍历角色的url 然后与访问url做匹配
        5. 无匹配返回权限不足
        :param request:
        :return:
        """
        # print(request.user)
        # print(request.user.is_superuser)
        path = request.path
        if "?" in path:
            path = path.split("?")[0]
        print(path)

        unlogin_exclude = ("/api/v1/user/login/", "/favicon.ico/", '/docs/')
        login_exclude = ("/api/v1/user/logout/",)

        if request.path in unlogin_exclude:
            return None
        if request.user.is_superuser:
            return None
        if request.user.is_anonymous:
            # return HttpResponseForbidden("请登录")
            return None
        if request.path in login_exclude:
            return None

        roles = request.user.roles.filter(status=True)
        # 得到所有的访问权限
        permissions = UrlPermission.objects.none()
        for role in roles:
            permissions |= role.permission.only("title", "method").filter(status=True)
        # 逻辑是循环所有 url  与 当前 url 做比对
        for p in permissions:
            # 必须路径匹配,然后 url 必须
            if p.url in path:
                if p.url == path and path == "/":
                    return None
                if p.url != "/" and (p.method == request.method or p.get_method_display() == "ALL"):
                    return None
        else:
            # api 与 页面
            if "/api/" in path:
                return HttpResponse(json.dumps({"code": 1, "msg": "权限不足！"}, ensure_ascii=False))
