"""
Django settings for swtProject project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


with open('env.json') as env:
    ENV = json.load(env)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-i%h@*13n--wf@5x5_gk0ekg5g^&mph^t2c*gmlq9u@of^s_+sw"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    "taskManager",
]


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    #     'rest_framework.permissions.IsAdminUser'
    #     'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
}



MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "swtProject.urls"


CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_HEADERS = ('*')
CORS_ALLOWED_ORIGINS=['http://127.0.0.1','http://127.0.0.1:5173','http://localhost:5173',
                        'https://api.bulbul559.cn', 'https://bulbul559.cn','https://api.youthol.online']


# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['127.0.0.1','127.0.0.1:5173','localhost:5173/','api.youthol.online',
                        'https://api.bulbul559.cn/', 'https://bulbul559.cn/','https://api.youthol.online/']


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "swtProject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': ENV['DATABASES']['NAME'],
        'USER': ENV['DATABASES']['USER'],
        'PASSWORD': ENV['DATABASES']['PASSWORD'],
        'HOST': ENV['DATABASES']['HOST'],
        'PORT': ENV['DATABASES']['PORT'],
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'MYSQL': {
            'driver': 'pymysql',
            'charset': 'utf8mb4',
        },
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"


USE_I18N = True

# 设置时区为中国标准时间
TIME_ZONE = 'Asia/Shanghai'

# 启用时区支持
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# 配置邮箱
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ENV['EMAIL']['HOST']  # 腾讯QQ邮箱SMTP服务器地址
EMAIL_PORT = ENV['EMAIL']['PORT']  # SMTP服务的端口号
EMAIL_HOST_USER = ENV['EMAIL']['USER']  # 发送邮件的0Q邮箱
EMAIL_HOST_PASSWORD = ENV['EMAIL']['PASSWORD']  # QQ邮箱授权码
EMAIL_USE_TLS = ENV['EMAIL']['USE_TLS']  # 与SMTP服务器通信时,是否启动TLS链接(安全链接)默认FaLse
