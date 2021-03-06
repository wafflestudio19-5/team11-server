"""
Django settings for everytime project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import datetime
import os
from pathlib import Path

#firebase
import firebase_admin
from firebase_admin import credentials
try:
    cred = credentials.Certificate("everytime/secret_firebase.json")
    firebase_admin.initialize_app(cred)
except FileNotFoundError:
    pass

SITE_ID=1

import json
from django.core.exceptions import ImproperlyConfigured

# local과 server의 설정 변수 분리
try :
    with open('everytime/secret.json', 'r') as f:
        secrets = json.loads(f.read())
except :
    secrets = ""

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)
    except TypeError:
        print("everytime/secret.json does not exist")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if "TEAM11_SERVER_ENV" in os.environ :
    print("env : server")
    SECRET_KEY = get_secret("SECRET_KEY")
    DEBUG = False
    ALLOWED_HOSTS = ['127.0.0.1',]
else: 
    print("env : local")
    SECRET_KEY = 'django-insecure-ax5v)%q)d*bl*78y6qw@9pn(=@5r83s5)+%3ufi4%eqf8og^cm'
    DEBUG = True
    ALLOWED_HOSTS = []


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG_TOOLBAR = os.getenv('DEBUG_TOOLBAR') in ('true', 'True')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'emailcode.apps.EmailCodeConfig',
    'university.apps.UniversityConfig',
    'department.apps.DepartmentConfig',
    'user.apps.UserConfig',
    'lecture.apps.LectureConfig',
    'review.apps.ReviewConfig',
    'information.apps.InformationConfig',
    'schedule.apps.ScheduleConfig',
    'customlecture.apps.CustomlectureConfig',

    'board.apps.BoardConfig',
    'article.apps.ArticleConfig',
    'comment.apps.CommentConfig',

    'message.apps.MessageConfig',

    'django.contrib.sites',
    'rest_framework',
    'django_extensions',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    
    'storages',
]
if "TEAM11_SERVER_ENV" in os.environ :
    AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID") # .csv 파일에 있는 내용을 입력 Access key ID
    AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY") # .csv 파일에 있는 내용을 입력 Secret access key
    AWS_REGION = get_secret("AWS_REGION")

    ###S3 Storages
    AWS_STORAGE_BUCKET_NAME = get_secret("AWS_STORAGE_BUCKET_NAME") # 설정한 버킷 이름
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME,AWS_REGION)

    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_S3_SECURE_URLS = False
    AWS_QUERYSTRING_AUTH = False

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_ROOT = os.path.join(BASE_DIR, '/images/')
    MEDIA_URL = '/images/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),

    'DEFAULT_PAGINATION_CLASS': 'common.pagination.CustomPagination',
    'PAGE_SIZE': 20
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
DEFAULT_FROM_MAIL = "waffle"

if "TEAM11_SERVER_ENV" in os.environ: 
    EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")
else: 
    EMAIL_HOST_USER = "johndoe@localhost.com"
    EMAIL_HOST_PASSWORD = "dummypassword"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'everytime.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'everytime.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
if "TEAM11_SERVER_ENV" in os.environ: 
    DATABASES = get_secret("DATABASES")
else: 
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '127.0.0.1',
            'PORT': 3306,
            'NAME': 'team11_db',
            'USER': 'team11_db_user',
            'PASSWORD': 'secretkey1234',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS' : {
            'min_length' : 8,
        }
    },
    {
        'NAME': 'common.validation.MaximumLengthValidator'
    },
    {
        'NAME': 'common.validation.PasswordFormValidator'
    }
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = STATIC_DIR


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'user.User'

JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',  # 암호화 알고리즘
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=28),  # 유효기간 설정 - app에서 login 유지
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=28),  # JWT 토큰 갱신 유효기간
}

# https://king-minwook.tistory.com/m/81?category=790110
if "TEAM11_SERVER_ENV" in os.environ :
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'debug.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console','file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.template': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }

SESSION_COOKIE_DOMAIN = '.wafl.shop'