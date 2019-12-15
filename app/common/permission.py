from rest_framework.permissions import BasePermission
from rest_framework_jwt.authentication import get_authorization_header, jwt_decode_handler
from user.models import UrlPermission, User
from jwt.exceptions import DecodeError, ExpiredSignatureError


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        # 获取，查询
        token = get_authorization_header(request)
        if not token:
            return False
        try:
            payload = jwt_decode_handler(token)

        except DecodeError as e:
            print(1,e)

            return False
        except ExpiredSignatureError:
            raise False

        user = User.get_by_id(payload["user_id"])
        if not user:
            return False

        if user.is_superuser:
            return True

        path = request.path
        if "?" in path:
            path = path.split("?")[0]

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
                    return True
                if p.url != "/" and (p.method == request.method or p.get_method_display() == "ALL"):
                    return True
        else:
            return False
