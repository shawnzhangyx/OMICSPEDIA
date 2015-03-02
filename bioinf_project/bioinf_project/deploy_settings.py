"""
Django settings for bioinf_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS 

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['OMICSPEDIA_SECRET_KEY']
# below is the old secret key. 
#SECRET_KEY = '69cno!47lp@*y9xzojy2@6sh**d#$!ry*0*_u8db6a#q@88usa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    'ones.ccmb.med.umich.edu',
]


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # django 3rd party apps
    'django_extensions',
    'crispy_forms',
    'django_select2',
    'south',
    # omicspedia specific apps
    'tags',
    'posts',
    'wiki',
    'software',
    'users',
    'meta',
    'utils',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #other middlewares
    'users.middleware.UpdateLastActivityMiddleware',
)

## template context processors:
TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS +(
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'bioinf_project.urls'

WSGI_APPLICATION = 'bioinf_project.wsgi.application'

## graph models
GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# for Heroku
import dj_database_url
DATABASES = {}
DATABASES['default'] =  dj_database_url.config()
if len(DATABASES['default']) ==0:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'sqlite.dat',
            }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

### this is for development server only 
MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles/media')

CRISPY_TEMPLATE_PACK = 'bootstrap3'

AUTO_RENDER_SELECT2_STATICS = False
SELECT2_BOOTSTRAP = True

AUTH_USER_MODEL = "users.User"

##### e-mail host and login 
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'omicspedia@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['OMICSPEDIA_HOST_PASSWORD'] 
EMAIL_PORT = 587
EMAIL_USE_TLS = True


CSRF_COOKIE_SECURE = False 
SESSION_COOKIE_SECURE = False

