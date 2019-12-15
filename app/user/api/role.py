import time
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from common.pagination import XadminPageLimitPagination
from common.response import JsonResponse
from ..serializer import RoleSerializer
from ..models import Role, UrlPermission, Menu
from common.exceptions import CodeError


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.order_by("id").all()
    serializer_class = RoleSerializer
    pagination_class = XadminPageLimitPagination
    lookup_url_kwarg = "id"

    def create(self, request, *args, **kwargs):
        title = request.data.get("title", None)
        status = request.data.get("status", True)
        if title:
            role = Role(title=title, status=status)
            role.save()
        else:
            raise CodeError("错误的参数")
        return Response({"message": "成功"})

    def update(self, request, *args, **kwargs):
        id = self.kwargs.get("id", None)
        role = get_object_or_404(Role, id=id)
        title = request.data.get("title", None)
        status = request.data.get("status", True)
        if title:
            if title != role.title:
                role.title = title
            elif status != role.status:
                role.status = status
            else:
                raise CodeError("没有变化！")
            role.save()
            return Response({"message": "成功"})
        raise CodeError("缺少参数！")

    def delete(self, request, **kwargs):
        print(request.data)
        if request.data:
            id_list = request.data.get("ids", [])
            if id_list is not []:
                for id in id_list:
                    role = Role.objects.filter(id=id).first()
                    if role:
                        role.delete()
        return Response({"message": "Success!"})


class ChangeRoleStatus(APIView):
    def get(self, request, **kwargs):
        id = request.GET.get("key")
        role = get_object_or_404(Role, id=id)
        role.status = not role.status
        role.save()
        return JsonResponse(code=0, msg="success")


class RolePermission(APIView):
    """ get请求得到该角色的已选权限和所有权限 post修改已选权限"""

    def get(self, request, **kwargs):
        """ 返回值 已选权限/全部权限"""
        id = self.kwargs.get("id", None)
        role = Role.objects.filter(id=id).first()
        role_permissions = []
        if role:
            role_id = [p.id for p in role.permission.all()]
        else:
            raise CodeError("未找到！")

        for permission in UrlPermission.objects.all():
            d = {
                "value": permission.id,
                "title": "%s %s:%s" % (permission.title, permission.url, permission.method),
            }
            role_permissions.append(d)
        return Response({"permissions": role_permissions, "checked": role_id})

    def post(self, request, **kwargs):
        id = self.kwargs.get("id", None)
        pids = request.data.get("ids", None)
        role = get_object_or_404(Role, id=id)
        try:
            role.permission.set(pids)
            role.save()
        except Exception as e:
            raise CodeError("出错" + str(e))
        return Response({"message": "success"})


class RoleMenu(APIView):
    def get(self, request, **kwargs):
        id = self.kwargs.get("id", None)
        role = Role.objects.filter(id=id).first()
        role_menus = []
        if role:
            role_id = [p.id for p in role.menu.all()]
        else:
            raise CodeError("未找到！")

        for menu in Menu.objects.all():
            d = {
                "value": menu.id,
                "title": "%s : %s" % (menu.title, menu.path),
            }
            role_menus.append(d)
        return Response({"menus": role_menus, "checked": role_id})

    def post(self, request, **kwargs):
        print(request.data)
        id = self.kwargs.get("id", None)
        mids = request.data.get("ids", None)
        role = get_object_or_404(Role, id=id)
        try:
            role.menu.set(mids)
            role.save()
        except Exception as e:
            raise CodeError("出错" + str(e))
        return Response({"message": "success"})


class Test(APIView):
    # authentication_classes = []
    permission_classes = []

    def get(self, request, **kwargs):
        # 返回登录者的角色的 菜单权限
        menus = Menu.objects.none()
        for role in request.user.roles.all():
            menus |= role.menu.all()

        user_menu = []
        for menu in menus:
            if menu.is_parent:
                c = {
                    "name": menu.name,
                    "icon": menu.icon,
                    "label": menu.title,
                    "url": menu.path,
                    "path": menu.url,
                    "children": []
                }
                # 父组件
                for m in menu.childrens.all():
                    if m in menus:
                        print('存在', m)
                        c["children"].append({
                            "name": m.name,
                            "icon": m.icon,
                            "label": m.title,
                            "url": m.path,
                            "path": m.url,
                        })
                user_menu.append(c)
        print(user_menu)

        return Response({"message": "ok"})
