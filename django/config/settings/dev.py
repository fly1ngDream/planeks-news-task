from .base import *


ALLOWED_HOSTS = ['*']


DEBUG = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<SECRET KEY>'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'planeks-news.sqlite3'),
    }
}
