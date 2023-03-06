from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from Machine.settings import BASE_DIR
from logs import logger
import os

# {BASE_DIR}
class HookDeployment(APIView):
    def post(self, request, *args, **kwargs):
        logger.info('============hook============')
        result = os.system("cd /home/zdh/test && touch test.vv")
        return Response(result)
