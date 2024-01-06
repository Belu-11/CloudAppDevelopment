"""
Django settings for djangobackend project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from decouple import config
import requests
from cloudant.client import Cloudant
from cloudant.error import CloudantException

from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from requests import ConnectionError

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from rest_framework.permissions import AllowAny
from corsheaders.middleware import CorsMiddleware

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# print(f"DEBUG: {config('DEBUG', default=False, cast=bool)}")
# print(f"SECRET_KEY: {config('SECRET_KEY')}")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'ao5z(o(z@cvzodm99d32jkxa5e8a1!q_4sqss5-a%n6tg$#h$+'
SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

APPEND_SLASH = True

ALLOWED_HOSTS = ["127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'djangoapp.apps.DjangoappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# React use in order to not block the react framework
REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.AllowAny']}

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'djangobackend.urls'

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
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangobackend.wsgi.application'


# NLU IBM
authenticator = IAMAuthenticator(config("NLU_API_KEY"))
version = '2022-04-07'
nlu = NaturalLanguageUnderstandingV1(
        version=version,
        authenticator=authenticator
)
nlu.set_service_url(config('NLU_URL'))

NLU_INSTANCE = nlu


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Cloudant Database Configuration
COUCH_USERNAME = config('COUCH_USERNAME')
IAM_API_KEY = config('IAM_API_KEY')
COUCH_URL = config('DB_URL')
COUCH_HOST = config('DB_HOST')
client = None


# try:
#     client = Cloudant.iam(
#         account_name=COUCH_USERNAME,
#         api_key=IAM_API_KEY,
#         connect=True,
#     )
#     print('Connect success! Connected to DB')
#     print(f"Databases: {client.all_dbs()}")
# except CloudantException as cloudant_exception:
#     print("unable to connect")
#     print(f"error {str(cloudant_exception)}")
# except (requests.exceptions.RequestException, ConnectionResetError) as err:
#     print("connection error")
#     print(f"error {str(err)}")

try:
    authenticator = IAMAuthenticator(IAM_API_KEY)
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(COUCH_URL)

    # print(f"Databases: {client.get_all_dbs().get_result()}")

    # print(f"client {str(client)}")
except CloudantException as cerr:
    print("Connection error occurred:")
    print(cerr)
except (requests.exceptions.RequestException, ConnectionResetError) as err:
    print("connection error")
    print(f"error {str(err)}")
except Exception as e:
    print("An error occured while connecting to db")
    print(f"error {str(e)}")


CLOUDANT_DB = client

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "OPTIONS": {
    #         "service": "my_service",
    #         "passfile": ".my_pgpass",
    #     },
    # }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': config('DB_NAME'),
    #     'USER': config('DB_USER'),
    #     'PASSWORD': config('DB_PASSWORD'),
    #     'HOST': config('DB_HOST'),
    #     'PORT': config('DB_PORT', default='5432'),
    # }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
MEDIA_URL = '/media/'

