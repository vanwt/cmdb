from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(Assets)
class AssetsAdmin(admin.ModelAdmin):
    list_display = ["id", "ip", "asset_type", "status", "create_time"]


@admin.register(IDC)
class IDCAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
