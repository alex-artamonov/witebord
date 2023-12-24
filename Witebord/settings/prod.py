from .base import *

DEBUG = False

ADMINS = [
    ('Alex Artamonov', 'alex.artamonov2010@gmail.com'),
]
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'witeboard2',
        'USER': 'witeboard',
        'PASSWORD': '12345',
        'PORT': '5432',
        'HOST': 'localhost',
    }
}