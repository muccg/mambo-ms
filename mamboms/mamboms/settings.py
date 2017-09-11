# -*- coding: utf-8 -*-
import os
import logging
import logging.handlers

from ccg_django_utils.conf import EnvConfig

env = EnvConfig()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCRIPT_NAME = env.get("script_name", os.environ.get("HTTP_SCRIPT_NAME", ""))
FORCE_SCRIPT_NAME = env.get("force_script_name", "") or SCRIPT_NAME or None


CCG_WRITEABLE_DIRECTORY = os.path.join(BASE_DIR,"scratch")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': env.get("dbuser", "webapp"),
        'NAME': env.get("dbname", "webapp"),
        'PASSWORD': env.get("dbpass", "webapp"),
        'HOST': env.get("dbhost", "db"),
        'PORT': env.get("dbport", ""),
    }
}

# see: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # !!!At the moment the app is not using CSRF!!!
    'django.middleware.csrf.CsrfViewMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# see: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = [
    'mamboms.mambomsapp',
    'mamboms.mambomsuser',
    'mamboms.util_scripts',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django_extensions',
    #'south',
    'djangosecure'
]

# these determine which authentication method to use
# apps use modelbackend by default, but can be overridden here
# see: https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
 'django.contrib.auth.backends.ModelBackend'
]

# We have a puppet function to generate these by hashing appname and a secret
SECRET_KEY = env.get("secret_key", "changeme")

# General site config
PRODUCTION = env.get("production", False)
DEBUG = env.get("debug", not PRODUCTION)

# Default SSL on and forced, turn off if necessary
SSL_ENABLED = env.get("ssl_enabled", PRODUCTION)
SSL_FORCE = env.get("ssl_force", PRODUCTION)

# django-secure
SECURE_SSL_REDIRECT = env.get("secure_ssl_redirect", PRODUCTION)
SECURE_HSTS_SECONDS = 500
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = env.get("secure_frame_deny", PRODUCTION)
SECURE_CONTENT_TYPE_NOSNIFF = env.get("secure_content_type_nosniff", PRODUCTION)
SECURE_BROWSER_XSS_FILTER = env.get("secure_browser_xss_filter", PRODUCTION)

# session and cookies
SESSION_COOKIE_AGE = env.get("session_cookie_age", 60 * 60)
SESSION_COOKIE_PATH = '{0}/'.format(SCRIPT_NAME)
SESSION_SAVE_EVERY_REQUEST = env.get("session_save_every_request", True)
SESSION_COOKIE_HTTPONLY = env.get("session_cookie_httponly", True)
SESSION_COOKIE_SECURE = env.get("session_cookie_secure", PRODUCTION)
SESSION_COOKIE_NAME = env.get(
    "session_cookie_name", "mambo_{0}".format(SCRIPT_NAME.replace("/", "")))
SESSION_COOKIE_DOMAIN = env.get("session_cookie_domain", "") or None

CSRF_COOKIE_NAME = env.get("csrf_cookie_name", "csrf_{0}".format(SESSION_COOKIE_NAME))
CSRF_COOKIE_DOMAIN = env.get("csrf_cookie_domain", "") or SESSION_COOKIE_DOMAIN
CSRF_COOKIE_PATH = env.get("csrf_cookie_path", SESSION_COOKIE_PATH)
CSRF_COOKIE_SECURE = env.get("csrf_cookie_secure", PRODUCTION)
CSRF_COOKIE_HTTPONLY = env.get("csrf_cookie_httponly", True)
CSRF_COOKIE_AGE = env.get("csrf_cookie_age", 31449600)
CSRF_FAILURE_VIEW = env.get("csrf_failure_view", "django.views.csrf.csrf_failure")
CSRF_HEADER_NAME = env.get("csrf_header_name", 'HTTP_X_CSRFTOKEN')
CSRF_TRUSTED_ORIGINS = env.getlist("csrf_trusted_origins", ['localhost'])

# Default the site ID to 1, even if the sites framework isn't being used
SITE_ID = 1

# see: https://docs.djangoproject.com/en/1.4/ref/settings/#root-urlconf
ROOT_URLCONF = 'mamboms.urls'

# This one's a constant, where puppet will have collect static files to
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#static-root
STATIC_ROOT=os.path.join(BASE_DIR, 'static')

# These may be overridden, but it would be nice to stick to this convention
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#static-url
STATIC_URL = '{0}/static/'.format(SCRIPT_NAME)

# settings used when FileSystemStorage is enabled
MEDIA_ROOT = env.get('media_root', os.path.join(BASE_DIR, 'uploads'))
MEDIA_URL = '{0}/uploads/'.format(SCRIPT_NAME)

# All templates must be loaded from within an app, so these are the only
# ones that should be enabled.
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#template-loaders
TEMPLATE_LOADERS = [
    'django.template.loaders.app_directories.Loader'
]

# Default all email to ADMINS and MANAGERS to root@localhost.
# Puppet redirects this to something appropriate depend on the environment.
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#admins
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#managers
ADMINS = [
    ('alerts', env.get("alert_email", "root@localhost"))
]
MANAGERS = ADMINS

# email
EMAIL_USE_TLS = env.get("email_use_tls", False)
EMAIL_HOST = env.get("email_host", 'smtp')
EMAIL_PORT = env.get("email_port", 25)
EMAIL_HOST_USER = env.get("email_host_user", "webmaster@localhost")
EMAIL_HOST_PASSWORD = env.get("email_host_password", "")
EMAIL_APP_NAME = env.get("email_app_name", "MAMBO {0}".format(SCRIPT_NAME))
EMAIL_SUBJECT_PREFIX = env.get("email_subject_prefix", "DEV {0}".format(SCRIPT_NAME))


# Default date input formats, may be overridden
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#date-input-formats
TIME_ZONE = env.get("time_zone", 'Australia/Perth')
LANGUAGE_CODE = env.get("language_code", 'en')
USE_I18N = False
USE_L10N = False
DATE_INPUT_FORMATS = ('%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y','%d %m %Y','%d %m %y', '%d %b %Y')
DATE_FORMAT = "d-m-Y"
SHORT_DATE_FORMAT = "d/m/Y"

# This honours the X-Forwarded-Host header set by our nginx frontend when
# constructing redirect URLS.
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#use-x-forwarded-host
USE_X_FORWARDED_HOST = env.get("use_x_forwarded_host", True)

if env.get("memcache", ""):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': env.getlist("memcache"),
            'KEY_PREFIX': env.get("key_prefix", "mambo")
        }
    }

    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'mambo_cache',
            'TIMEOUT': 3600,
            'MAX_ENTRIES': 600
        }
    }

    SESSION_ENGINE = 'django.contrib.sessions.backends.file'
    SESSION_FILE_PATH = CCG_WRITABLE_DIRECTORY

# Log directory created and enforced by puppet
CCG_LOG_DIRECTORY = env.get('log_directory', os.path.join(BASE_DIR, "log"))

# Default logging configuration, can be overridden
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(name)s:%(levelname)s:%(asctime)s:%(filename)s:%(lineno)s:%(funcName)s] %(message)s'
        },
        'db': {
            'format': '[%(name)s:%(duration)s:%(sql)s:%(params)s] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(filename)s:%(lineno)s (%(funcName)s)  %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file':{
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(CCG_LOG_DIRECTORY, 'mamboms.log'),
            'when': 'midnight',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'include_html':True
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file', ],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'mamboms': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    }
}

#-=-=-=-=-=-=-=-=-=-=-#

# see: https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = '{0}/login/'.format(SCRIPT_NAME)
LOGOUT_URL = '{0}/logout/'.format(SCRIPT_NAME)
LOGIN_REDIRECT_URL = '{0}/'.format(SCRIPT_NAME)

PERSISTENT_FILESTORE = CCG_WRITEABLE_DIRECTORY #os.path.normpath(os.path.join(PROJECT_DIRECTORY, 'files'))
PERSISTENT_FILESTORE_URL = '/mamboms/files/'

AUTH_PROFILE_MODULE = 'mambomsuser.MambomsLDAPProfile'

#-=-=-=-=-=-=-=-=-=-=-#

try:
    print "Attempting to import local settings as appsettings.mamboms"
    from appsettings.mamboms import *
    print "Successfully imported appsettings.mamboms"
except ImportError, e:
    print "Failed to import appsettings.mamboms"
