from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.db import IntegrityError
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from common import serializers, pagination
from common.response import JsonResponse
from ..models import Assets, IDC
from user.models import User
from ..filters import AssetsFilterSet
from common.exceptions import CodeError


# Create your views here.
# 增改单独的，因为前端框架不一样所以无法使用自带的
class AssetsInfoViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Assets.objects.order_by("create_time").exclude(status=0)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = AssetsFilterSet
    pagination_class = pagination.XadminPageLimitPagination
    serializer_class = serializers.AssetsInfoSerializer

    def get_queryset(self):
        asset_type = self.request.GET.get("type", "3")
        if asset_type == "1":
            queryset = Assets.objects.select_related("idc", "host_machine", "user", "opsuser").defer("change_time") \
                .prefetch_related("tags").filter(asset_type=1).exclude(status=0)
        elif asset_type == "2":
            queryset = Assets.objects.select_related("idc", "host_machine", "user", "opsuser").defer("change_time") \
                .prefetch_related("tags").filter(asset_type=2).exclude(status=0)
        else:
            queryset = Assets.objects.prefetch_related("tags").select_related("idc", "host_machine", "user",
                                                                              "opsuser").all()
        # 得到的queryset 再判断 是否 符合此用户
        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(Q(user=self.request.user) | Q(opsuser=self.request.user))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(code=0, msg="success", data=serializer.data)


class AssetsViewSet(ModelViewSet):
    """ 上面的资产视图是吧序列化后的资产信息列出来，用于展示数据表等，此时图用于展示根本数据"""

    queryset = Assets.objects.order_by("create_time").exclude(status=0)
    pagination_class = pagination.VuePageLimitPagination
    serializer_class = serializers.AssetsSerializer

    def get_queryset(self):
        asset_type = self.request.GET.get("type", "3")
        if asset_type == "1":
            queryset = Assets.objects.select_related("idc", "host_machine", "user", "opsuser").defer("change_time") \
                .prefetch_related("tags").filter(asset_type=1).exclude(status=0)
        elif asset_type == "2":
            queryset = Assets.objects.select_related("idc", "host_machine", "user", "opsuser").defer("change_time") \
                .prefetch_related("tags").filter(asset_type=2).exclude(status=0)
        else:
            queryset = Assets.objects.prefetch_related("tags").select_related("idc", "host_machine", "user",
                                                                              "opsuser").all()
        # 得到的queryset 再判断 是否 符合此用户
        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(Q(user=self.request.user) | Q(opsuser=self.request.user))

    def delete(self, request, **kwargs):
        """
        参数 ids => list
        可实现删除多个
        """
        if request.data:
            id_list = request.data.get("ids", [])
            if id_list is not []:
                for id in id_list:
                    asset = Assets.objects.filter(id=id).first()
                    if asset:
                        if asset.status != 0:
                            asset.status = 0
                            asset.save()
                        else:
                            asset.delete()

        return Response("删除成功")

    def create(self, request, *args, **kwargs):
        """
        创建资产
        """
        asset = Assets()
        try:
            asset.ip = request.data.get("ip")
            asset.asset_type = request.data.get("asset_type")
            asset.status = request.data.get("status")
            asset.system = request.data.get("system")
            asset.remark = request.data.get("remark")
            asset.sshuser = request.data.get("sshuser")
            asset.verify_type = int(request.data.get("verify_type"))
            asset.sshpwd = request.data.get("sshpwd")
            asset.sshport = request.data.get("sshport")
            asset.mysql_user = request.data.get("mysql_user")
            asset.mysql_pwd = request.data.get("mysql_pwd")
            asset.mysql_port = request.data.get("mysql_port")
            asset.ftp_port = request.data.get("ftp_port")
            # 关联
            id = request.data.get("host_machine")
            if id:
                asset.host_machine = Assets.objects.filter(id=id).first()

            opsid = request.data.get("opsuser")
            if opsid:
                asset.opsuser = User.objects.filter(id=opsid).first()

            userid = request.data.get("user")
            if userid:
                asset.user = User.objects.filter(id=userid).first()

            idc_id = request.data.get("idc")
            if idc_id:
                asset.idc = IDC.objects.filter(id=idc_id).first()
            asset.save()
        except IntegrityError as e:
            raise CodeError("重复添加")
        else:
            # 注册 tag
            tags = request.data.get("tag")
            if tags:
                tags = tags.split(",")

                asset.tags.set(tags)
                asset.save()
        return Response("添加成功")

    def update(self, request, *args, **kwargs):
        """ 修改资产的数据 """
        id = self.kwargs.get("pk", None)
        print(request.data)
        asset = Assets.objects.filter(id=id).first()
        if asset:
            try:
                asset.ip = request.data.get("ip")
                asset.asset_type = request.data.get("asset_type")
                asset.status = request.data.get("status")
                asset.system = request.data.get("system")
                asset.remark = request.data.get("remark")
                asset.sshuser = request.data.get("sshuser")
                asset.verify_type = int(request.data.get("verify_type"))
                asset.sshpwd = request.data.get("sshpwd")
                asset.key = request.data.get("sshkey")
                asset.sshport = request.data.get("sshport")
                asset.mysql_user = request.data.get("mysql_user")
                asset.mysql_pwd = request.data.get("mysql_pwd")
                asset.mysql_port = request.data.get("mysql_port")
                asset.ftp_port = request.data.get("ftp_port")
                # 关联
                id = request.data.get("host_machine")
                if id:
                    asset.host_machine = Assets.objects.filter(id=id).first()
                else:
                    asset.host_machine = None
                opsid = request.data.get("opsuser")
                if opsid:
                    asset.opsuser = User.objects.filter(id=opsid).first()
                else:
                    asset.opsuser = None
                userid = request.data.get("user")
                if userid:
                    asset.user = User.objects.filter(id=userid).first()
                else:
                    asset.user = None

                idc_id = request.data.get("idc")
                if idc_id:
                    asset.idc = IDC.objects.filter(id=idc_id).first()
                else:
                    asset.idc = None
                asset.save()
            except IntegrityError as e:
                raise CodeError(str(e))
            else:
                # 注册 tag
                tags = request.data.get("tags")
                if tags:
                    tags = tags.split(",")

                    asset.tags.set(tags)
                    asset.save()
                code = 0
                msg = "success"
        else:
            raise CodeError("未找到!")
        return Response("添加成功")


class ServerCount(APIView):
    def get(self, request, **kwargs):
        num = Assets.objects.filter(asset_type=1).count()
        return Response({"num": num})


class VmCount(APIView):
    def get(self, request, **kwargs):
        num = Assets.objects.filter(asset_type=2).count()
        return Response({"num": num})
