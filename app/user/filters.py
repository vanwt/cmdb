from django_filters import FilterSet, CharFilter, DateFilter
from .models import User


class UserFilter(FilterSet):
    username = CharFilter(field_name="username", lookup_expr="icontains")
    realname = CharFilter(field_name="realname", lookup_expr="icontains")
    phone = CharFilter(field_name="phone", lookup_expr="icontains")
    end = DateFilter(field_name="last_login", lookup_expr="lte")
    start = DateFilter(field_name="last_login", lookup_expr="gte")

    class Meta:
        model = User
        fields = ["realname", "username", "phone", "start", "end"]
