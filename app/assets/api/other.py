from rest_framework.views import APIView
from common.response import JsonResponse
from paramiko import SSHClient, AutoAddPolicy

class TestConnectApiView(APIView):

    def get(self, request, **kwargs):
        msg = "错误的参数"
        code = 1
        host = request.GET.get("host", None)
        password = request.GET.get("pwd", None)
        user = request.GET.get("user", "root")
        port = request.GET.get("port", 22)
        if host and user and password and port:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy)
            try:
                ssh.connect(hostname=host, username=user, password=password, port=port, timeout=5)
            except Exception as e:
                print(e)
                msg = str(e)
                code = 1
            else:
                code = 0
                msg = None
                ssh.close()

        return JsonResponse(code=code, msg=msg)
