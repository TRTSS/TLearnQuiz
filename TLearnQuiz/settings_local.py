# SECURITY WARNING: keep the secret key used in production secret!
from pathlib import Path

SECRET_KEY = 'django-insecure-ub8r!xabw@6f2qxcs472)nkxh(@cl2(m73_a#j7upav1qfh!vw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

HOST = 'http://127.0.0.1:8000'

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
