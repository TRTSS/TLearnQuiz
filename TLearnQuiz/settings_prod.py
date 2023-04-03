# SECURITY WARNING: keep the secret key used in production secret!
from pathlib import Path

SECRET_KEY = 'django-insecure-ub8r!xabw@erf34xdvbc)nkxh(@cl2(m73_a#j7upav1qfh!vw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '89.111.136.90', 'zuvs.ru']

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tlearnquiz',
        'USER': 'quizadmin',
        'PASSWORD': 'Red159753tie!',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
