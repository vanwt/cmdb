from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def all_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['message'] = response.data["detail"]
    return response




class CodeError(APIException):
    status_code = 400
