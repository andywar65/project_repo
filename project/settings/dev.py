from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SERVER_EMAIL = 'me@examplecom'
DEFAULT_FROM_EMAIL = 'me@examplecom'
DEFAULT_RECIPIENT = 'andy.war1965@gmail.com'

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('DEV_DB_NAME'),
        'USER': 'postgres',
        'PASSWORD': '09w5t43w',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(APPLICATION_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(APPLICATION_DIR, 'media')
MEDIA_URL = '/media/'

PRIVATE_STORAGE_ROOT = os.path.join(APPLICATION_DIR, 'private-media')
PRIVATE_STORAGE_AUTH_FUNCTION = 'private_storage.permissions.allow_authenticated'

REST_API_TARGET = 'https://rifondazionepodistica.it/wp-json/wp/v2/'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://127.0.0.1:8000'

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']


try:
    from .local import *
except ImportError:
    pass
