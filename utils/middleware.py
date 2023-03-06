import json
import time

from logs import logger
from django.utils.deprecation import MiddlewareMixin


class LogMiddle(MiddlewareMixin):
    def process_request(self, request):
        # 存放请求过来时的时间
        request.init_time = time.time()

        # 请求方式
        method = request.method

        # 请求用户
        user = request.user

        # 参数类型
        content_type = request.content_type
        try:
            param = str(request.body, encoding="utf-8")
            param = json.loads(param) if param else param
        except UnicodeDecodeError as e:
            param = str(dict(request.POST))
        except Exception as e:
            param = []



        try:
            host = request.META['HTTP_HOST']
        except Exception as e:
            host = '0.0.0.0'
        # 获取ip地址
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        # 请求路径
        path = request.get_full_path_info()
        header = f"""--------------------------------------------------
                [ HEADER ] (
                 'METHOD'       => {method},
                 'HOST'         => {host}
                 'PATH'         => {path},
                 'PARMA'        => {param},
                 'USER'         => {user},
                 'ip'           => {ip},
                 'content_type' => {content_type}
                 )
                  """
        logger.info(header)

    def process_response(self, request, response):
        # data = response.data
        # status_code = response.status_code
        # status_text = response.status_text
        # response = f"""
        #         [ Response ] (
        #          'status_code'  => {status_code},
        #          'msg'          => {status_text},
        #          'data'         => {data}
        #          )
        #           """
        # logger.info(response)
        logger.info(f"{'=' * 50}【RunTime:{round(time.time() - request.init_time, 2)}s】")
        return response

    def process_exception(self, request, exception):
        logger.exception(exception)
        return
