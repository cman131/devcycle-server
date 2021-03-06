# Django settings for dataCollection project.

import os
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

#GEOS_LIBRARY_PATH = 'C:\\OSGeo4W\\bin\\geos_c.dll'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'DCS',
#        'NAME':'dev_test1',
        'USER': 'dev',
        'PASSWORD': 'password',
        'HOST': 'localhost',
#        'HOST':'cycl-ops.se.rit.edu',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/static/'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    '/usr/local/devcycle-server/tour_config/static/',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@qpn)xr0i2sy8v1i4va@c_30#q$xjj_2^crh)wf$+w4=y@#ep_'

#CSRF_COOKIE_DOMAIN = 'localhost' #your domain name

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.core.context_processors.csrf'
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dataCollection.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dataCollection.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_PATH + '/Templates',
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    #'admin.processor_file_name.user',
    "django.core.context_processors.media",
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rider',
    'location_update',
    'tour_config',
    'rest_framework',
    'south',
    'djcelery',
    'analysis',
    #'bootstrap_toolkit',

    'django_admin_bootstrapped',
    'django.contrib.admin',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'django-logs/default.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'django-logs/requests.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {

        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'filters': {
#        'require_debug_false': {
#            '()': 'django.utils.log.RequireDebugFalse'
#        }
#    },
#    'handlers': {
#        'mail_admins': {
#            'level': 'ERROR',
#            'filters': ['require_debug_false'],
#            'class': 'django.utils.log.AdminEmailHandler'
#        },
#        'console': {
#            'level': 'DEBUG',
#            'class': 'logging.StreamHandler',
#        },
#    }
#}


KEY = '52af783df367b7a5c7d01457d82544bf'
SALT = '58268845878249858254353589767595'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}

JSON_KEYS = {
    'RIDER_ID': u'rider_id',
    'RIDER_OS': u'os',
    'RIDER_PUSH_ID': u'push_id',
    'LOCATIONS': u'locations',
    'LOC': {
        'LON': u'longitude',
        'LAT': u'latitude',
        'ACC': u'accuracy',
        'BEARING': u'bearing',
        'SPEED': u'speed',
        'BATT_LVL': u'battery',
        'PROVIDER': u'provider',
        'TIME': u'time'
    },
    'BAD_REQ': u'bad_request',
    'TOUR_CONFIG': u'config',
    'SERVER_POLLING_RATE' : u'server_polling_rate',
    'SERVER_POLLING_RANGE' : u'server_polling_range',
    'LOCATION_POLLING_RATE' : u'location_polling_rate',
}

#celery
import djcelery
djcelery.setup_loader()

BROKER_URL = 'amqp://guest:guest@localhost:5672//'

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'runs-every-10-minuets': {
        'task': 'location_update.tasks.update_num_riders',
        'schedule': timedelta(minutes=10),
#        'schedule': timedelta(seconds=5),
    },
    'runs-every-5-minuets': {
        'task': 'location_update.tasks.build_all_speed',
        'schedule': timedelta(minutes=5),
    },
}

GCM_SEND_URL = 'https://android.googleapis.com/gcm/send'
GCM_API_KEY_HEADER = 'Authorization'
GCM_API_KEY = 'AIzaSyAQAY5vKcs8c3h-Js_Tl38d97MMCJ4aHE4'
#DEFAULT_MAP_LAT = 40.72931
#DEFAULT_MAP_LON = -73.99979
DEFAULT_MAP_LAT = 43.0844
DEFAULT_MAP_LON = 77.6749
#MAP_TILE_SERVER = 'http://cycl-ops.se.rit.edu'
MAP_TILE_SERVER = 'http://otile1.mqcdn.com/tiles/1.0.0'
