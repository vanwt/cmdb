from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import Tags
from common import serializers
from common.pagination import XadminPageLimitPagination


class TagViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = XadminPageLimitPagination

    def delete(self, request, **kwargs):
        if request.data:
            id_list = request.data.get("ids", [])
            for id in id_list:
                role = Tags.objects.filter(id=id).first()
                if role:
                    role.delete()
        return Response({"message": "Success!"})
