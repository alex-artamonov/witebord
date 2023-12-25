from .base import *

ALLOWED_HOSTS = ['localhost', 
                 '127.0.0.1', 
                 '0.0.0.0:8000']
DEBUG = False

ADMINS = [
    ('Alex Artamonov', 'alex.artamonov2010@gmail.com'),
]

#DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'witeboard2',
#         'USER': 'witeboard',
#         'PASSWORD': '12345',
#         'PORT': '5432',
#         'HOST': '0.0.0.0',
#     }
# }

DATABASES = {
'default': {
}
}