from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import jwt_decode_handler
from user.models import User
import jwt


class JsonWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        # 获取token
        token = get_authorization_header(request)
        if not token:
            raise AuthenticationFailed("Token 认证失败!")
        try:
            payload = jwt_decode_handler(token)
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationFailed("Token 失效")
        except jwt.exceptions.DecodeError:
            raise AuthenticationFailed("非法的 Token")

        user = User.get_by_id(payload["user_id"])

        if user:
            return user, token
        else:
            raise AuthenticationFailed("没有此用户，请联系管理员！")
