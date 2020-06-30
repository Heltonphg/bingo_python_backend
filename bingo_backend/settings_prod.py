from .settings import *

DEBUG = False

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'bingo'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'frede1618@@'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': '5432',
    }
}