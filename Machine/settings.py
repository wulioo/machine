"""
Django settings for Machine project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os, sys

import datetime

# 获得当前时间
now = datetime.datetime.now()
# 转换为指定的格式
otherStyleTime = now.strftime("%Y_%m_%d")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@jm*uk0ynybqy&-ch89ew^o4eal5$m0v#mi$_$d(5)9svgitc1'
FIXTURE_DIRS = (f'{BASE_DIR}/fixtures/',)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'user.User'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_filters",
    'rest_framework',
    'corsheaders',

    'extra.db',
    'apps.future',
    'apps.equity',

    'apps.user',
    'apps.system',
    'apps.hook',
    'apps.monitor',
    'apps.fv_sequential',
    'apps.api_fv_sequential',
    'apps.api_fv_section',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 这里是新增的中间件
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middleware.LogMiddle'
]
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "utils.exception.custom_exception_handler",
    # 全局过滤器
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
}

ROOT_URLCONF = 'Machine.urls'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# 跨域允许的操作
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
# 跨域允许的请求头
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': []
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Machine.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "tq_ml_sys",
        'USER': 'daihuizheng',
        'PASSWORD': "Iry7X+pP7D0E+A==",
        'HOST': "192.168.1.160",
        'PORT': "3306",
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        },

    },

    'tqmain': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': "192.168.1.160",
        'NAME': "tqmain",
        'USER': 'daihuizheng',
        'PASSWORD': "Iry7X+pP7D0E+A==",
        'PORT': "3306",

    },
    'tq_factor': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': "192.168.1.160",
        'NAME': "tq_factor",
        'USER': 'daihuizheng',
        'PASSWORD': "Iry7X+pP7D0E+A==",
        'PORT': "3306",
    },
    'tq_signal': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': "192.168.1.154",
        'NAME': "tq_signal",
        'USER': 'daihuizheng',
        'PASSWORD': "Iry7X+pP7D0E+A==",
        'PORT': "3306",
    },
    'tq_daily_drv': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': "192.168.1.160",
        'NAME': "dws_tq_daily_drv",
        'USER': 'daihuizheng',
        'PASSWORD': "Iry7X+pP7D0E+A==",
        'PORT': "3306",
    },

    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': "machine",
    #     'USER': 'root',
    #     'PASSWORD': "c298b8c3aa41c3c8",
    #     'HOST': "192.168.1.166",
    #     'PORT': "3306",
    #
    # },
    # 'tqmain': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'HOST': "192.168.1.166",
    #     'NAME': "tqmain",
    #     'USER': 'root',
    #     'PASSWORD': "c298b8c3aa41c3c8",
    #     'PORT': "3306",
    #
    # },
    # 'tq_factor': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'HOST': "192.168.1.166",
    #     'NAME': "tq_factor",
    #     'USER': 'root',
    #     'PASSWORD': "c298b8c3aa41c3c8",
    #     'PORT': "3306",
    # },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=30),
}

PROCESS_NUM = 12
# CELERY_RESULT_BACKEND = 'rpc://'
# CELERY_BROKER_URL = "amqp://admin:admin@192.168.1.166:5672/myvhost"

CELERY_RESULT_BACKEND = 'redis://:aa1234bb@127.0.0.1:6379/2'
CELERY_BROKER_URL = 'redis://:aa1234bb@127.0.0.1:6379/1'
# CELERY_BROKER_URL = "amqp://admin:admin@192.168.1.166:5672/myvhost"
CELERY_DISABLE_RATE_LIMITS = True
CELERY_WORKER_CONCURRENCY = PROCESS_NUM
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 43200}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:aa1234bb@127.0.0.1:6379",
        "TIMEOUT": 1800,  # 设置redis过期时间 2天 1800
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "decode_responses": True,
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 500,
                # 'timeout': 20,
            },  # 池的个数
            # "PASSWORD": "aa1234bb"
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# logging 简单日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志模块
    'formatters': {
        'verbose': {
            'format': '{asctime} [ {module}:{lineno:d} ] [ {levelname} ] {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        "default": {
            "format": '%(asctime)s %(name)s  %(pathname)s:%(lineno)d %(module)s:%(funcName)s '
                      '%(levelname)s- %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        # 'file': {  # 定义日志文件记录
        #     'level': 'INFO',
        #     'class': 'logging.FileHandler',
        #     'filename': os.path.join(BASE_DIR, 'logs\debug.log'),
        #     'formatter': 'verbose',  # 输出简单的样式
        # 'filename': os.path.join(BASE_DIR, 'logs', 'err.log'),  # 定义日志文件目录,logs文件夹没有就创建,err.log自动生成

        # 'when': 'D',  # 每天切割一次日志
        # 'interval': 1,  # 时间间隔: 一天
        # 'backupCount': 10,  # 保留?份日志
        # 'encoding': 'utf-8'
        # },
        'console': {  # 定义终端打印记录
            'level': 'DEBUG',  # 打印所有信息
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',  # 输出简单的样式
        },
        "db_backends": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, f'logs\\runtime_ {otherStyleTime}.log'),
            'formatter': 'verbose'
        },

    },

    'loggers': {
        # 'django': {  # 定义了一个名为django的日志器
        #     'handlers': ['console', 'file'],  # 可以同时在终端跟文件中输出
        #     'level': 'INFO',
        #     'propagate': True,
        # },
        "django.db.backends": {  # django db记录
            "level": "DEBUG",
            "handlers": ["db_backends", 'console'],
            'propagate': False,
        },
        # 'log': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # }
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
