from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import uuid


# Create your models here.
class UrlPermission(models.Model):
    METHODS = (
        ("GET", "GET"), ("POST", "POST"), ("PUT", "PUT"), ("DELETE", "DELETE"), ("ALL", "ALL")
    )
    title = models.CharField(max_length=64, blank=True)
    url = models.CharField(max_length=128, null=True, blank=True, help_text="url与method 联合唯一")
    status = models.BooleanField(default=True, blank=True)
    method = models.CharField(max_length=32, choices=METHODS, default="GET", blank=True)
    objects = models.Manager

    class Meta:
        db_table = "ops_permission"
        unique_together = ("url", "method")
        verbose_name = "权限表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<%s : %s>" % (self.title, self.get_method_display())


class Menu(models.Model):
    """ 菜单权限表 """
    title = models.CharField(max_length=64, blank=True)
    path = models.CharField(verbose_name="路径", blank=True, null=True, max_length=64)
    url = models.CharField(verbose_name="组件路径", null=True, blank=True, max_length=32)
    name = models.CharField(verbose_name="别名", null=True, blank=True, max_length=32)
    icon = models.CharField(verbose_name="图标", null=True, blank=True, max_length=32)
    status = models.BooleanField(default=True, blank=True)
    is_parent = models.BooleanField(verbose_name="是否未父组件", default=False, blank=True)
    parent = models.ForeignKey("self", related_name="childrens", db_constraint=False, on_delete=models.SET_NULL,
                               null=True, blank=True)
    objects = models.Manager

    class Meta:
        db_table = "ops_menu"
        verbose_name = "菜单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Role(models.Model):
    """ 角色表 """
    title = models.CharField(max_length=64, blank=True)
    menu = models.ManyToManyField(Menu, related_name="role", db_constraint=False, blank=True)
    permission = models.ManyToManyField(UrlPermission, related_name="role", db_constraint=False, blank=True)
    users = models.ManyToManyField("user.User", related_name="roles", db_constraint=False, blank=True)
    status = models.BooleanField(default=True, blank=True)

    objects = models.Manager

    class Meta:
        db_table = "ops_role"
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class User(AbstractUser):
    """用户表"""
    id = models.UUIDField(verbose_name="用户ID", default=uuid.uuid4, primary_key=True, editable=False)
    password = models.CharField('password', max_length=128, blank=True, null=True)
    phone = models.CharField('手机号', max_length=11, null=True, blank=True)
    realname = models.CharField('真实姓名', max_length=32, null=False)
    job_number = models.CharField('工号', max_length=128, null=False)
    is_active = models.BooleanField(verbose_name='是否激活', default=True, null=True)
    avatar = models.CharField(verbose_name='用户头像', max_length=255, null=True, blank=True)
    info = models.CharField(verbose_name='介绍', null=True, max_length=100, blank=True)

    token = models.CharField(verbose_name="钉钉唯一标识符", max_length=128, blank=True)
    userid = models.CharField(verbose_name="钉钉用户id", max_length=128, blank=True, null=True)

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    change_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.realname:
            return self.realname
        else:
            return self.username

    @staticmethod
    def get_by_id(id):
        return User.objects.filter(id=id).first()
