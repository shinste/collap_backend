"""
Django settings for collap project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from rest_framework.permissions import AllowAny
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get('SECRET_KEY')
# SECRET_KEY = 'django-insecure--p9_2ew#3-z2elx#l&rh$)wq)899%$_zap$#^10l(n*7&6d*qb'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOST").split(' ')
# ALLOWED_HOSTS = ['localhost', 'collap-backend.onrender.com']
#'127.0.0.1'
# ALLOWED_HOSTS = []

# SECURE_HSTS_SECONDS = 31536000

# CSRF_COOKIE_AGE = 8 * 3600           


# CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]
# CSRF_ALLOWED_ORIGINS = ["http://localhost:3000"]
# CORS_ORIGINS_WHITELIST = ["http://localhost:3000"]
# CORS_ALLOW_CREDENTIALS = True

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE = 'None'
# SESSION_COOKIE_SAMESITE = 'None'
# CORS_ORIGIN_ALLOW_ALL = False
# CORS_ALLOW_CREDENTIALS = True
# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'corsheaders'
]
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles') ## deploy setting
SECRET_KEY = '13XdxKHyyK'
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']]
DEBUG = False
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# DEVELOPER SETTINGS
# SECRET_KEY = 'django-insecure--p9_2ew#3-z2elx#l&rh$)wq)899%$_zap$#^10l(n*7&6d*qb'
# DEBUG = True
# ALLOWED_HOSTS = []


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', ##deploy setting
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Use the full path to the AllowAny class
    ],
    # Other DRF settings...
}

ROOT_URLCONF = 'collap.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'collap.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# database_url = os.environ.get("DATABASE_URL")
# DATABASES["default"] = dj_database_url.parse("postgres://collap_postgresql_db_user:4hDFC0YklQTToPlcGXBJ7z506BFDi3Sf@dpg-cmffcsen7f5s73c4vi40-a.oregon-postgres.render.com/collap_postgresql_db")
#postgres://collap_postgresql_db_user:4hDFC0YklQTToPlcGXBJ7z506BFDi3Sf@dpg-cmffcsen7f5s73c4vi40-a.oregon-postgres.render.com/collap_postgresql_db

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "https://master--illustrious-unicorn-98eadd.netlify.app"
#     # Add other origins if needed
# ]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Local development
    "https://master--illustrious-unicorn-98eadd.netlify.app",
    "http://master--illustrious-unicorn-98eadd.netlify.app",
    "https://master--illustrious-unicorn-98eadd.netlify.app/registration",
    "https://master--illustrious-unicorn-98eadd.netlify.app/"
]