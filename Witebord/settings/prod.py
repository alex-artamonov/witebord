import os
from .base import *

DEBUG = False

ADMINS = [
    ('Alex Artamonov', 'alex.artamonov2010@gmail.com'),
]

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'witeboard2',
#         'USER': 'witeboard',
#         'PASSWORD': '12345',
#         'PORT': '5432',
#         'HOST': '0.0.0.0',
#     }
# }

