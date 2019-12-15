from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from common.pagination import XadminPageLimitPagination
from common.response import JsonResponse
from ..filters import UserFilter
from ..models import User, Role
from ..serializer import UserSerializer
from common.exceptions import CodeError


class LogoutApiView(APIView):
    def get(self, request, **kwargs):
        logout(request)
        return JsonResponse({"code": 0, "msg": "Success !"})


class UserApiView(ModelViewSet):
    queryset = User.objects.order_by("last_login").all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = UserFilter
    pagination_class = XadminPageLimitPagination
    lookup_url_kwarg = "id"

    def create(self, request, *args, **kwargs):
        code = 0
        msg = None
        username = request.data.get("username", None)
        realname = request.data.get("realname", None)
        many = request.data.get("many", 'false')
        password = request.data.get("password", None)
        phone = request.data.get("phone", None)
        email = request.data.get("email", None)
        remark = request.data.get("remark", None)
        print(request.data)
        if many == "true":
            msg_list = []
            usernames = username.split("|")
            realnames = realname.split("|")
            if len(usernames) == len(realnames):
                for i in range(len(usernames)):
                    user = User()
                    try:
                        user.username = usernames[i]
                        user.realname = realnames[i]
                        user.password = make_password(password)
                        user.email = email
                        user.phone = phone
                        user.save()
                    except IntegrityError as e:
                        msg_list.append("用户" + realnames[i] + "创建失败 " + str(e))
                else:
                    msg = "创建成功 ! ," + "|".join(msg_list)
                    return JsonResponse(code=code, msg=msg)
            else:
                return JsonResponse(code=1, msg="账户名与姓名不匹配!")
        else:
            user = User()
            try:
                user.username = username
                user.realname = realname
                user.password = make_password(password)
                user.email = email
                user.phone = phone
                user.info = remark
                user.save()
            except IntegrityError as e:
                code = 1
                msg = str(e)

        return JsonResponse(code=code, msg=msg)

    def update(self, request, *args, **kwargs):
        code = 0
        msg = "修改成功"
        id = self.kwargs.get("id", None)
        user = User.objects.filter(id=id).first()

        username = request.data.get("username", None)
        realname = request.data.get("realname", None)
        phone = request.data.get("phone", None)
        email = request.data.get("email", None)
        remark = request.data.get("remark", None)
        if user:
            try:
                user.username = username
                user.realname = realname
                user.email = email
                user.phone = phone
                user.info = remark
                user.save()
            except IntegrityError as e:
                code = 1
                msg = str(e)
            return JsonResponse(code=code, msg=msg)
        msg = "未找到!"
        return JsonResponse(code=1, msg=msg)

    def delete(self, request, **kwargs):
        print(request.data)
        if request.data:
            id_list = request.data.get("ids", [])
            for id in id_list:
                user = User.objects.filter(id=id).only("username").first()
                if user and user.username != request.user.username:
                    # 删除的用户不能是当前正在使用的用户
                    user.delete()
        return Response({"message": "Success"})


class UserChaneRole(APIView):

    def get(self, request, **kwargs):
        id = self.kwargs.get("key")
        user = get_object_or_404(User, id=id)
        roles = []
        for role in Role.objects.all():
            d = {
                "value": role.id,
                "title": role.title
            }
            roles.append(d)
        selected = [role.id for role in user.roles.all()]
        msg = {"roles": roles, "selected": selected}
        return Response(msg)

    def put(self, request, **kwargs):
        id = self.kwargs.get("key")
        user = get_object_or_404(User, id=id)
        selected = request.data.get("selected")
        try:
            user.roles.set(selected)
        except Exception as e:
            raise CodeError("修改失败:" + str(e))

        return Response({"message": "success!"})
