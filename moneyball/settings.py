"""
Django settings for moneyball project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(BASE_DIR,'moneyball/common/static')
STATIC_URL = '/common/static/'
STATICFILES_DIRS=(
    ("cssmainsite",os.path.join(STATIC_ROOT,'mainsite')),
    ("csslogin",os.path.join(STATIC_ROOT,'login')),
    ("js",os.path.join(STATIC_ROOT,'js')),
    ("images",os.path.join(STATIC_ROOT,'images')),
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xtdkofon6-u4rvx^+u)g^1**dg853yvzciea4b=r535_-j0=te'

# SECURITY WARNING: don't run with debug turned on in production!
if socket.gethostname() == 'CHANGSHU2':
    DEBUG = TEMPLATE_DEBUG = True
else:
    DEBUG = TEMPLATE_DEBUG = False
    ALLOWED_HOSTS = ['moneyball.com.cn', 'www.moneyball.com.cn']

#DEBUG = TEMPLATE_DEBUG = True
ADMINS = (
    ('chang', '13690578@qq.com'),
)
MANAGERS = (
    ('chang', '13690578@qq.com'),
)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.exmail.qq.com'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'passwordreset@moneyball.com.cn'
# EMAIL_HOST_PASSWORD = 'moneyball001'
# EMAIL_USE_TLS = True
# EMAIL_SUBJECT_PREFIX = u'[Moneyball]'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'moneyball.reset@gmail.com'
EMAIL_HOST_PASSWORD = 'moneyball001'
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = u'[Moneyball]'

TEMPLATE_DEBUG = True

#ALLOWED_HOSTS = ['58.247.181.229']
#ALLOWED_HOSTS = ['localhost', '127.0.0.1']
#ALLOWED_HOSTS = ['moneyball.com.cn', 'www.moneyball.com.cn']


LOGIN_URL = "/login"

LOGIN_REDIRECT_URL = "/login"

# Application definition
# AUTH_USER_MODEL = 'user.MyUser'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pagination',
    'moneyball.common',
    'moneyball.common.templatetags',
    'moneyball.user',
    'moneyball.loan',
    'moneyball.wx',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

# Context processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)
ROOT_URLCONF = 'moneyball.urls'

WSGI_APPLICATION = 'moneyball.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'moneyball',
        'USER': 'postgres',
        'PASSWORD': '1Qaz2wsx3edc',
#         'HOST': 'www.moneyball.com.cn',
        'HOST': 'localhost',
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

