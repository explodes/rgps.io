import os

rel = lambda *x: os.path.abspath(os.path.join(os.path.dirname(__file__), '..', *x))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': rel('database.db'),
    }
}