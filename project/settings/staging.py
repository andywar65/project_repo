import os
import json
from django.core.exceptions import ImproperlyConfigured
from .base import *

with open(os.path.join(PROJECT_DIR, 'settings/secrets.json')) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    '''Get the secret variable or return explicit exception.
    Thanks to twoscoopsofdjango'''
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(setting)
        raise ImproperlyConfigured(error_msg)

DEBUG = False

ALLOWED_HOSTS = [
    'digitalkomix.com',
    'www.digitalkomix.com',
]

WSGI_APPLICATION = 'rpnew_prog.wsgi_stag.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

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
SERVER_EMAIL = 'no_reply@rifondazionepodistica.it'
DEFAULT_FROM_EMAIL = 'no_reply@rifondazionepodistica.it'
DEFAULT_RECIPIENT = 'rifondazionepodistica96@gmail.com'

STATIC_ROOT = '/home/andywar65/apps/rpnew_static'# no trailing slash
STATIC_URL = 'https://digitalkomix.com/static/'

MEDIA_ROOT = '/home/andywar65/apps/rpnew_media'# no trailing slash
MEDIA_URL = 'https://digitalkomix.com/media/'

SECRET_KEY = get_secret('SECRET_KEY')

REST_API_TARGET = 'https://rifondazionepodistica.it/wp-json/wp/v2/'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'https://digitalkomix.com'

try:
    from .local import *
except ImportError:
    pass
