import datetime
import json
import os
import pickle
import time
import uuid

import pandas as pd
import pymysql
from celery import shared_task
from django.core.cache import cache
from matplotlib import pyplot as plt

from Machine.settings import STATICFILES_DIRS, BASE_DIR
from logs import logger
from service.ndcg import Ndcg
from utils.common import TimeContext


@shared_task
def celery_restart_django():

    os.system(f'echo "aa1234bb" | uwsgi --reload {BASE_DIR}/script/uwsgi.pid')
    return 'success'





