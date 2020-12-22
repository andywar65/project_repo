from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    get_secret('ALLOWED_HOSTS'),
    'www.' + get_secret('ALLOWED_HOSTS'),
]

WSGI_APPLICATION = 'project.wsgi_prod.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',#this is different!
        'NAME': get_secret('NAME'),
        'USER': get_secret('USER'),
        'PASSWORD': get_secret('PASSWORD'),
        'HOST': get_secret('HOST'),
        'PORT': get_secret('PORT'),
    },
}

RECAPTCHA_PUBLIC_KEY = get_secret('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = get_secret('RECAPTCHA_PRIVATE_KEY')

# Mail configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = get_secret('EMAIL_HOST')
EMAIL_PORT = get_secret('EMAIL_PORT')
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
SERVER_EMAIL = get_secret('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = get_secret('DEFAULT_FROM_EMAIL')
DEFAULT_RECIPIENT = get_secret('DEFAULT_RECIPIENT')

STATIC_ROOT = get_secret('STATIC_ROOT')# no trailing slash
STATIC_URL = get_secret('BASE_URL') + '/static/'

MEDIA_ROOT = get_secret('MEDIA_ROOT')# no trailing slash
MEDIA_URL = get_secret('BASE_URL') + '/media/'

PRIVATE_STORAGE_ROOT = get_secret('PRIVATE_STORAGE_ROOT')
PRIVATE_STORAGE_AUTH_FUNCTION = get_secret('PRIVATE_STORAGE_AUTH_FUNCTION')

REST_API_TARGET = get_secret('REST_API_TARGET') + '/wp-json/wp/v2/'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = get_secret('BASE_URL')

MAPBOX_TOKEN = get_secret('MAPBOX_TOKEN')

try:
    from .local import *
except ImportError:
    pass
