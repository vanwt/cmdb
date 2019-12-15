from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from .models import Assets, Tags
from user.models import User


class AssetsFilterSet(FilterSet):
    ip = CharFilter(field_name="ip", lookup_expr="icontains")
    sshuser = CharFilter(field_name="sshuser", lookup_expr="icontains")
    mysql_user = CharFilter(field_name="mysql_user", lookup_expr="icontains")
    mysql_port = CharFilter(field_name="mysql_port", lookup_expr="icontains")
    tags = CharFilter(method="many_tags_filter")
    opsuser = ModelChoiceFilter(queryset=User.objects.all())
    kefu = ModelChoiceFilter(queryset=User.objects.all())
    end = DateFilter(field_name="create_time", lookup_expr="lte")
    start = DateFilter(field_name="create_time", lookup_expr="gte")

    def many_tags_filter(self, queryset, name, value):
        # 自定义过滤
        if "," in value:
            values = value.split(",")
            for v in values:
                queryset = queryset.filter(tags=v)
                if not queryset:
                    return queryset
            return queryset
        else:
            return queryset.filter(tags=value)

    class Meta:
        model = Assets
        fields = ["ip", "start", "end", "tags", "mysql_user", "mysql_port", "sshuser", "opsuser", "kefu"]
