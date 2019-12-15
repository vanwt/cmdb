from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response


class VuePageLimitPagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_query_param = "page"
    max_page_size = 200

    def paginate_queryset(self, queryset, request, view=None):
        self.count = len(queryset)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('data', data),
        ]))


class XadminPageLimitPagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_query_param = "page"
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        self.count = len(queryset)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        code = 0
        msg = "success"
        if not data:
            code = 1
            msg = "not found !"
        return Response(OrderedDict([
            ('code', code),
            ('msg', msg),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
        ]))
