from rest_framework import serializers
from assets.models import Assets, Tags, IDC


class AssetsInfoSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    asset_type = serializers.CharField(source="get_asset_type_display")
    verify_type = serializers.CharField(source="get_verify_type_display")
    host_machine = serializers.SerializerMethodField()
    user = serializers.CharField()
    opsuser = serializers.CharField()
    tags = serializers.SerializerMethodField()
    idc = serializers.SerializerMethodField()

    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    change_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def get_idc(self, obj):
        if obj.idc:
            return obj.idc.name
        else:
            return None

    def get_host_machine(self, obj):
        if obj.host_machine:
            return obj.host_machine.ip
        return None

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    class Meta:
        model = Assets
        fields = ["id", "ip", "status", "mac", "is_pass", "asset_type", "verify_type", "idc", "tags", 'sshuser',
                  "sshport", "mysql_user", "system", "mysql_port", "mysql_pwd", "ftp_port", "host_machine",
                  "create_time", "change_time", "user", "opsuser", "remark", ]
        read_only_fields = ["ip", "create_time"]

    def __str__(self):
        return self.ip


class AssetsSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    change_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    asset_type = serializers.CharField()
    status = serializers.CharField()
    verify_type = serializers.CharField()

    class Meta:
        model = Assets
        fields = "__all__"
        read_only_fields = ["ip", "create_time"]

    def __str__(self):
        return self.ip


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ["id", "name"]


class IDCSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDC
        fields = ["id", "name"]
