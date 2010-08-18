# -*- coding: utf-8 -*-
# Django settings for project.
import os
from django.utils.webhelpers import url

# PROJECT_DIRECTORY isnt set when not under wsgi
if not os.environ.has_key('PROJECT_DIRECTORY'):
    os.environ['PROJECT_DIRECTORY']=os.path.dirname(__file__).split("/appsettings/")[0]

from appsettings.default_dev import *
from appsettings.mamboms.dev import *

# Login/logout URLS and redirect
LOGIN_URL = url('/login/')
LOGIN_REDIRECT_URL = url('/')
LOGOUT_URL = url('/logout')

SSL_FORCE = True

# mamboms uses a slightly different set of middleware, so define here
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.email.EmailExceptionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.ssl.SSLRedirect',
    'django.middleware.cache.FetchFromCacheMiddleware'
)

##
## cache middleware settings
##
CACHE_BACKEND = 'memcached://memcache1.localdomain:11211;memcache2.localdomain:11211/'
CACHE_MIDDLEWARE_SECONDS = 5
CACHE_MIDDLEWARE_KEY_PREFIX = "mamboms-development-"

##
## CAPTCHA settings
##
CAPTCHA_IMAGES = os.path.join(WRITABLE_DIRECTORY, "captcha")
# the filesystem space to write the captchas intoo# Captcha image directory
CAPTCHA_ROOT = os.path.join(MEDIA_ROOT, 'captchas')
# the URL base that points to that directory served out
CAPTCHA_URL = os.path.join(MEDIA_URL, 'captchas')

AUTH_PROFILE_MODULE = 'mambomsuser.MambomsLDAPProfile'
LOGS = ['mango_ldap']
TEST_RUNNER = 'mamboms.test.testrunner.run_mamboms_tests'

##
## Everything from here should be fairly typical ccg/django app
##

ROOT_URLCONF = 'mamboms.urls'

INSTALLED_APPS.extend( [
    'mamboms.mambomsapp',
    'mamboms.mambomsuser',
    'django.contrib.admin',
    'django.contrib.auth'
] )

# Django will 'fall through' with its auth structure. What order do you want these?
# Do you want them at all? In production, its a good idea to switch off model backend
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.LDAPBackend',
    'django.contrib.auth.backends.NoAuthModelBackend',
    #'django.contrib.auth.backends.ModelBackend',
]

#
# You may wish to uncomment these two lines
# but make sure you have a good working database with session table before you save_every_request
#
SESSION_COOKIE_PATH = url('/')
SESSION_SAVE_EVERY_REQUEST = True

PERSISTENT_FILESTORE = os.path.normpath(os.path.join(PROJECT_DIRECTORY, '..', '..', 'files')) 
PERSISTENT_FILESTORE_URL = url('/mamboms/files/')

# which directory we put the processed files in
OUTPUT_SUBPATH = "output"
UPLOAD_SUBPATH = "upload"

if "LOCALDEV" in os.environ:
    SSL_ENABLED = False
    PERSISTENT_FILESTORE = os.path.normpath('/tmp/mambomsapp/filedata')

if not os.path.exists(os.path.join(PERSISTENT_FILESTORE,OUTPUT_SUBPATH)):
    os.mkdir(os.path.join(PERSISTENT_FILESTORE,OUTPUT_SUBPATH))

#Ensure the persistent storage dir exits. If it doesn't, exit noisily.
assert os.path.exists(PERSISTENT_FILESTORE), "This application cannot start: It expects a writeable directory at %s to use as a persistent filestore" % (PERSISTENT_FILESTORE) 
