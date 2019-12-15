from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import IDC
from common import serializers
from common.pagination import XadminPageLimitPagination


class IDCViewSet(ModelViewSet):
    queryset = IDC.objects.all()
    serializer_class = serializers.IDCSerializer
    pagination_class = XadminPageLimitPagination

    def delete(self, request, **kwargs):
        if request.data:
            id_list = request.data.get("ids", [])
            for id in id_list:
                role = IDC.objects.filter(id=id).first()
                if role:
                    role.delete()
        return Response({"message": "Success!"})
