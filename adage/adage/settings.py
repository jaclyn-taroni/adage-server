"""
Django settings for adage project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Any deployment configuration settings (including all secrets)
# come from config.py, which is never checked into source control. If we're
# running under Codeship we build a CONFIG on the fly using config.py.template
if os.environ.get('CODESHIP_SETTINGS') == 'YES':
    with open(os.path.join(BASE_DIR, 'adage', 'config.py.template')) as f:
        exec f
    CONFIG = CI_CONFIG
    pg_user = os.environ.get('PG_USER')
    pg_pass = os.environ.get('PG_PASSWORD')
    CONFIG['dbmaster']['USER'] = pg_user
    CONFIG['dbmaster']['PASSWORD'] = pg_pass
    CONFIG['databases']['default']['USER'] = pg_user
    CONFIG['databases']['default']['PASSWORD'] = pg_pass
else:
    from config import CONFIG

# Quick-start development settings - unsuitable for production
# TODO: review Django deployment checklist
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG['django_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'tastypie',
    'analyze',
)

# NOTE: to get tastypie to play nicely with Django 1.8, need to install using
# > pip install -e
#   git+https://github.com/django-tastypie/django-tastypie#egg=TastyPie
# see <https://github.com/django-tastypie/django-tastypie/issues/1290>
# for details
API_LIMIT_PER_PAGE = 50
TASTYPIE_FULL_DEBUG = True

HAYSTACK_CONNECTIONS = CONFIG['haystack']
# HAYSTACK_DEFAULT_OPERATOR = 'OR'
# TODO what is HAYSTACK_SEARCH_RESULTS_PER_PAGE doing for us?
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

# define and activate an Elasticsearch Custom Analyzer that mimics Snowball
# but adds a word_delimiter token filter where we want it (fixes bitbucket
# issue #1: "search on PA14 does not find E-GEOD-24262")
ELASTICSEARCH_DEFAULT_ANALYZER = "adage_snowball"
ELASTICSEARCH_INDEX_SETTINGS = {
    'settings': {
        "analysis": {
            "analyzer": {
                "adage_snowball": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "standard",
                        "word_delimiter",
                        "lowercase",
                        "stop",
                        "snowball"
                    ]
                },
            }
        }
    }
}

# adjust the default kwargs passed to Elasticsearch when searching
ELASTICSEARCH_DEFAULT_KWARGS = {
    'highlight': {
        'pre_tags': ['<strong>'],
        'post_tags': ['</strong>']
    }
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'adage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'adage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = CONFIG['databases']


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '/static/'),
)
