from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..serializer import PermissionSerializer
from common.pagination import XadminPageLimitPagination
from ..models import UrlPermission
from common.response import JsonResponse
from common.exceptions import CodeError


class PermissionViewSet(ModelViewSet):
    queryset = UrlPermission.objects.order_by("id").all()
    serializer_class = PermissionSerializer
    pagination_class = XadminPageLimitPagination
    lookup_url_kwarg = "id"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(code=0, msg="success", data=serializer.data)

    def create(self, request, *args, **kwargs):
        title = request.data.get("title", None)
        status = request.data.get("status", True)
        url = request.data.get("url", None)
        method = request.data.get("method", None)
        if title and url and method:
            try:
                p = UrlPermission(title=title, status=status, method=method, url=url)
                p.save()
            except Exception as e:
                raise CodeError(str(e))
            return Response({"message": "成功"})
        raise CodeError("验证失败")

    def update(self, request, *args, **kwargs):
        id = self.kwargs.get("id", None)
        p_obj = get_object_or_404(UrlPermission, id=id)

        title = request.data.get("title", None)
        url = request.data.get("url", None)
        method = request.data.get("method", None)
        status = request.data.get("status", True)
        if p_obj and title and url and method:
            try:
                p_obj.title = title
                p_obj.url = url
                p_obj.method = method
                p_obj.status = status
                p_obj.save()
            except Exception as e:
                raise CodeError(str(e))
        return Response({"message": "修改成功"})

    def delete(self, request, **kwargs):
        if request.data:
            id_list = request.data.get("ids", [])
            if id_list is not []:
                for id in id_list:
                    permission = UrlPermission.objects.filter(id=id).first()
                    if permission:
                        permission.delete()
        return Response({"message": "成功"})


class ChangePermissionStatus(APIView):
    def get(self, request, **kwargs):
        id = request.GET.get("key")
        p = get_object_or_404(UrlPermission, id=id)
        p.status = not p.status
        p.save()
        return JsonResponse(code=0, msg="success")
