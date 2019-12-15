from django.contrib import admin
from .models import User, Role, Menu, UrlPermission


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "realname", "create_time"]

    def __str__(self):
        return self.realname


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]

    def __str__(self):
        return self.title


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]

    def __str__(self):
        return self.title


@admin.register(UrlPermission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]

    def __str__(self):
        return self.title
