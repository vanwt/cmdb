from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from ..models import Menu
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..serializer import MenuSerializer
from common.pagination import XadminPageLimitPagination
from ..models import UrlPermission
from common.response import JsonResponse
from common.exceptions import CodeError


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = XadminPageLimitPagination
    lookup_url_kwarg = "id"

    def get_queryset(self):
        if self.kwargs.get("id"):
            return Menu.objects.order_by("id").all()
        else:
            return Menu.objects.order_by("id").filter(is_parent=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(code=0, msg="success", data=serializer.data)

    def update(self, request, *args, **kwargs):
        id = self.kwargs.get("id", None)
        m_obj = get_object_or_404(Menu, id=id)
        title = request.data.get("title", None)
        url = request.data.get("url", None)
        path = request.data.get("path", None)
        name = request.data.get("name", None)
        icon = request.data.get("icon", None)
        status = request.data.get("status", True)
        is_parent = request.data.get("is_parent", True)
        if status == "true":
            status = True
        else:
            status = False

        if is_parent == "true":
            is_parent = True
        else:
            is_parent = False
        parent = request.data.get("parent", None)
        p = Menu.objects.filter(id=parent).first()
        if title and url and path and name:
            try:
                m_obj.title = title
                m_obj.url = url
                m_obj.path = path
                m_obj.status = status
                m_obj.icon = icon
                m_obj.is_parent = is_parent
                m_obj.parent = p
                m_obj.save()
            except Exception as e:
                raise CodeError(str(e))
        return Response({"message": "修改成功"})

    def delete(self, request, **kwargs):
        if request.data:
            id_list = request.data.get("ids", [])
            if id_list is not []:
                for id in id_list:
                    menu = Menu.objects.filter(id=id).first()
                    if menu:
                        menu.delete()
        return Response({"message": "成功"})
