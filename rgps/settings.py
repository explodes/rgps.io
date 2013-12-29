import os

rel = lambda *x: os.path.abspath(os.path.join(os.path.dirname(__file__), '..', *x))

BASE_DIR = rel()
SECRET_KEY = '2=u1b)gxns$^6kedxf8=vo0=%_@=vsx7@5enjmq^bd#)9%$bv)'
DEBUG = False
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'rgps.app',
    'rgps.api',
    'rgps.push',
)

AUTH_USER_MODEL = "app.User"

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'rgps.push.context.settings',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'rgps.urls'
WSGI_APPLICATION = 'rgps.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Denver'
USE_I18N = False
USE_L10N = False
USE_TZ = True

MEDIA_ROOT = rel('media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    rel('templates'),
)

GPS_UPDATE_FRQ = 2500
GPS_UPDATE_COUNT = 60

ALLOWED_HOSTS = ['*']

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    rel('static'),
)

try:
    from local_settings import *
except ImportError:
    pass