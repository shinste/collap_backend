import os

from .settings import *  # noqa
from .settings import BASE_DIR
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
# ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']

STATIC_ROOT = BASE_DIR/'staticfiles'

STORAGES = {
    "default" : {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]


# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conn_str_params['name'],
        'HOST': conn_str_params['host'],
        'USER': conn_str_params['user'],
        'PASSWORD': conn_str_params['password'],
        'PORT': 5432
    }
}

# CACHES = {
#         "default": {  
#             "BACKEND": "django_redis.cache.RedisCache",
#             "LOCATION": os.environ.get('AZURE_REDIS_CONNECTIONSTRING'),
#             "OPTIONS": {
#                 "CLIENT_CLASS": "django_redis.client.DefaultClient",
#                 "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
#         },
#     }
# }
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 9999
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
