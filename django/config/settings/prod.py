from .base import *


ALLOWED_HOSTS = ['*']


DEBUG = False


SECRET_KEY = os.getenv('SECRET_KEY')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'planeks_news',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
