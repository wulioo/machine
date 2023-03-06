import array

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from Machine.settings import DEBUG


class CommonException(Exception):
    """公共异常类"""
    code = 500
    msg = '服务器内部错误'
    data = []
    status = status.HTTP_400_BAD_REQUEST,

    def __init__(self, code: int = None, msg: str = None, data: list = None):
        if code is not None:
            self.code = code

        if msg is not None:
            self.msg = msg

        if data is not None:
            self.msg = data
        self.data = data  # 状态码枚举类
        super().__init__()

    def __str__(self):
        return self.msg


class ResultEmpty(CommonException):
    code = 400
    msg = 'Result is None'


class ModelEmpty(CommonException):
    code = 400
    msg = 'Table is None'

def custom_exception_handler(exc, context):
    # 这里对自定义的 CustomException 直接返回，保证系统其他异常不受影响
    if isinstance(exc, CommonException):
        return Response(data={'code': exc.code, 'msg': exc.msg, 'data': exc.data}, status=exc.status[0])
    if isinstance(exc, ValidationError):
        return Response(data={'code': 400, 'msg': exc.args[0], 'data': None}, status=exc.status_code)
    return exception_handler(exc, context)
