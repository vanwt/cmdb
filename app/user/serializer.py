from rest_framework import serializers
from .models import User, Role, UrlPermission, Menu


class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return [[role.id, role.title] for role in obj.roles.all()]

    class Meta:
        model = User
        fields = ["id", "username", "realname", "email", "phone", "info", "last_login", "roles"]


class RoleSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    permission = serializers.SerializerMethodField()

    def get_permission(self, obj):
        return [per.id for per in obj.permission.all()]

    def get_users(self, obj):
        return [u.id for u in obj.users.all()]

    class Meta:
        model = Role
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlPermission
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    key = serializers.SerializerMethodField()

    def get_children(self, obj):
        if obj.is_parent:
            result = []
            menus = obj.childrens.all()
            i = 1
            for m in menus:
                result.append({
                    "key": str(obj.id) + str(i),
                    "id": m.id,
                    "title": m.title,
                    "name": m.name,
                    "path": m.path,
                    "url": m.url,
                    "icon": m.icon,
                    "status": m.status
                })
                i += 1
            return result
        else:
            return None

    def get_key(self, obj):
        return obj.id

    class Meta:
        model = Menu
        fields = "__all__"
