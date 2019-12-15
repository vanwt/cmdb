from django.db import models
from user.models import User
import uuid


class Assets(models.Model):
    """ 资产信息表"""
    ASSET_STATUS = (
        (0, '下架'), (1, '启用'), (2, '故障'), (3, '未使用'), (4, '未知')
    )
    SERVER_TYPE_CHOICES = (
        (1, '物理机'),
        (2, '虚拟机'),
        (3, 'Docker')
    )

    VERIFY_TYPE = (
        (0, "password"), (1, "key")
    )

    # 定义uuid 为自增主键
    id = models.UUIDField(verbose_name="ID", primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.GenericIPAddressField(verbose_name="管理IP", unique=True, null=True, db_index=True, blank=True)
    # 联合唯一 ip/mac
    mac = models.CharField(verbose_name="MAC地址", max_length=128, null=True, blank=True)

    # 主要
    status = models.PositiveIntegerField(verbose_name='设备状态', default=1, choices=ASSET_STATUS, blank=True)
    asset_type = models.PositiveIntegerField(choices=SERVER_TYPE_CHOICES, verbose_name="资产类型", blank=True, )
    system = models.CharField(max_length=128, verbose_name="操作系统", blank=True)
    is_pass = models.BooleanField(default=False, verbose_name="Ping", blank=True)

    # 关联
    tags = models.ManyToManyField("assets.Tags", verbose_name="标签", db_constraint=False, blank=True)
    idc = models.ForeignKey("assets.IDC", null=True, on_delete=models.SET_NULL, verbose_name="所属机房",
                            db_constraint=False, blank=True)
    host_machine = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="宿主机")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="used_assets", null=True, blank=True,
                             db_constraint=False,
                             verbose_name="使用者")
    opsuser = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="ops_assets", null=True, blank=True,
                                db_constraint=False,
                                verbose_name="管理者")

    # 软件信息
    verify_type = models.SmallIntegerField(choices=VERIFY_TYPE, default=0, verbose_name="验证类型", blank=True)
    sshuser = models.CharField(max_length=64, null=True, blank=True, verbose_name='SSH用户')
    sshport = models.CharField(max_length=5, null=True, blank=True, default=22, verbose_name='SSH端口')
    sshpwd = models.CharField(max_length=256, null=True, blank=True, verbose_name='密码验证')
    sshkey = models.CharField(max_length=256, null=True, blank=True, verbose_name="密匙")

    mysql_user = models.CharField(max_length=64, default='root', blank=True, verbose_name='MYSQL用户')
    mysql_pwd = models.CharField(max_length=128, null=True, blank=True, verbose_name='MYSQL密码')
    mysql_port = models.CharField(max_length=6, null=True, blank=True, default=3306, verbose_name='MYSQL端口')
    ftp_port = models.CharField(max_length=5, null=True, blank=True, verbose_name='FTP端口')

    remark = models.TextField(verbose_name='备注信息', blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    change_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, null=True, blank=True)

    # 上架/到期时间
    maturity_time = models.DateField(verbose_name="到期时间", null=True, blank=True)
    add_time = models.DateField(verbose_name="上架时间", null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = 'ops_assets'
        verbose_name_plural = verbose_name = '总资产表'

    def __str__(self):
        return self.ip


class IDC(models.Model):
    """IDC资产信息"""

    IDC_OPERATOR = (
        (0, u"电信"),
        (1, u"联通"),
        (2, u"移动"),
        (3, u"铁通"),
        (4, u"小带宽"),
    )
    name = models.CharField(max_length=128, unique=True, verbose_name="机房名称")
    linkphone = models.CharField(max_length=16, blank=True, null=True, verbose_name="联系电话")
    address = models.CharField(max_length=128, blank=True, null=True, verbose_name="机房地址")
    network_segment = models.TextField(blank=True, null=True, verbose_name="网段")
    bandwidth = models.CharField(max_length=64, blank=True, null=True, verbose_name="机房带宽")
    operator = models.PositiveIntegerField(verbose_name="运营商", choices=IDC_OPERATOR, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    change_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    objects = models.Manager

    class Meta:
        db_table = 'ops_idc'
        verbose_name_plural = verbose_name = 'IDC资产表'

    def __str__(self):
        return self.name


class Tags(models.Model):
    """资产标签"""

    name = models.CharField(max_length=64, blank=True, null=True, unique=True, verbose_name="标签")
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    objects = models.Manager

    class Meta:
        db_table = "ops_tags"
        verbose_name = "资产标签表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
