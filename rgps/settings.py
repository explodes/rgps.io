import os

rel = lambda *x: os.path.abspath(os.path.join(os.path.dirname(__file__), '..', *x))

BASE_DIR = rel()
SECRET_KEY = '2=u1b)gxns$^6kedxf8=vo0=%_@=vsx7@5enjmq^bd#)9%$bv)'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'rgps.app',
)

AUTH_USER_MODEL = "app.User"

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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': rel('database.db'),
    }
}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Denver'
USE_I18N = False
USE_L10N = False
USE_TZ = True

MEDIA_ROOT = rel('media')
MEDIA_URL = '/media/'

STATIC_ROOT = rel('static')
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    rel('templates'),
)

try:
    from local_settings import *
except ImportError:
    pass