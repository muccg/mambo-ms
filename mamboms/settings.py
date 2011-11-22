# -*- coding: utf-8 -*-
### BEGIN COPYRIGHT ###
#
# (C) Copyright 2011, Centre for Comparative Genomics, Murdoch University.
# All rights reserved.
#
# This product includes software developed at the Centre for Comparative Genomics 
# (http://ccg.murdoch.edu.au/).
# 
# TO THE EXTENT PERMITTED BY APPLICABLE LAWS, YABI IS PROVIDED TO YOU "AS IS," 
# WITHOUT WARRANTY. THERE IS NO WARRANTY FOR YABI, EITHER EXPRESSED OR IMPLIED, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND 
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT OF THIRD PARTY RIGHTS. 
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF YABI IS WITH YOU.  SHOULD 
# YABI PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR
# OR CORRECTION.
# 
# TO THE EXTENT PERMITTED BY APPLICABLE LAWS, OR AS OTHERWISE AGREED TO IN 
# WRITING NO COPYRIGHT HOLDER IN YABI, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR 
# REDISTRIBUTE YABI AS PERMITTED IN WRITING, BE LIABLE TO YOU FOR DAMAGES, INCLUDING 
# ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE 
# USE OR INABILITY TO USE YABI (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR 
# DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES 
# OR A FAILURE OF YABI TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER 
# OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
# 
### END COPYRIGHT ###

import os
from ccg.utils.webhelpers import url

# set debug, see: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# see: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# mamboms uses a slightly different set of middleware, so define here
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.ssl.SSLRedirect',
    'django.middleware.cache.FetchFromCacheMiddleware'
)

INSTALLED_APPS.extend( [
    'mamboms.mambomsapp',
    'mamboms.mambomsuser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django_extensions',
    'south'
] )

# see: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'mamboms.urls'

# these determine which authentication method to use
# yabi uses modelbackend by default, but can be overridden here
# see: https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# code used for additional user related operations
# see: https://docs.djangoproject.com/en/dev/ref/settings/#auth-profile-module
AUTH_PROFILE_MODULE = 'mambomsuser.MambomsLDAPProfile'

# cookies
# see: https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-age
# see: https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-name
SESSION_COOKIE_AGE = 60*60
SESSION_COOKIE_PATH = url('/')
SESSION_COOKIE_NAME = 'mamboms_sessionid'
SESSION_SAVE_EVERY_REQUEST = True
CSRF_COOKIE_NAME = "csrftoken_mamboms"

# Locale
# see: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
#      https://docs.djangoproject.com/en/dev/ref/settings/#language-code
#      https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
TIME_ZONE = 'Australia/Perth'
LANGUAGE_CODE = 'en-us'
USE_I18N = True

# see: https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = url('/login/')
LOGIN_REDIRECT_URL = url('/')
LOGOUT_URL = url('/logout')

### static file management ###
# see: https://docs.djangoproject.com/en/dev/howto/static-files/
# deployment uses an apache alias
STATICFILES_DIRS = []
STATIC_ROOT = os.path.join(PROJECT_DIRECTORY,"static")
STATIC_URL = url('/static/')
ADMIN_MEDIA_PREFIX = url('/static/admin/')

# media directories
# see: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = os.path.join(PROJECT_DIRECTORY,"static","media")
MEDIA_URL = url('/static/media/')

# a directory that will be writable by the webserver, for storing various files...
WRITABLE_DIRECTORY = os.path.join(PROJECT_DIRECTORY,"scratch")

# see: https://docs.djangoproject.com/en/dev/ref/settings/#append-slash
APPEND_SLASH = True

## CAPTCHA settings
##
# the filesystem space to write the captchas into
CAPTCHA_ROOT = os.path.join(MEDIA_ROOT, 'captchas')

# the url base that points to that directory served out
CAPTCHA_URL = os.path.join(MEDIA_URL, 'captchas')

# captcha image directory
CAPTCHA_IMAGES = os.path.join(WRITABLE_DIRECTORY, "captcha")

# see: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG

# see: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'ccg.template.loaders.makoloader.filesystem.Loader'
]

# see: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = [
    os.path.join(PROJECT_DIRECTORY,"templates"),
]

# mako compiled templates directory
MAKO_MODULE_DIR = os.path.join(WRITABLE_DIRECTORY, "templates")

# mako module name
MAKO_MODULENAME_CALLABLE = ''


### USER SPECIFIC SETUP ###
# these are the settings you will most likely change to reflect your setup


# see: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'USER': '',
        'NAME': 'yabiadmin.sqlite3',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Make this unique, and don't share it with anybody.
# see: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = 'set_this'

# email settings so yabi can send email error alerts etc
# see https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = 'set_this'
EMAIL_APP_NAME = "Mamboms "
SERVER_EMAIL = "apache@set_this"                      # from address
EMAIL_SUBJECT_PREFIX = "DEV "

# admins to email error reports to
# see: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ( 'alert', 'alerts@set_this.com' )
]

# see: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# memcache server list
# add a list of your memcache servers
MEMCACHE_SERVERS = ['localhost.localdomain:11211']
MEMCACHE_KEYSPACE = "mamboms-"

# uncomment to use memcache for sessions, be sure to have uncommented memcache settings above
# see https://docs.djangoproject.com/en/dev/ref/settings/#session-engine
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHE_BACKEND = 'memcached://'+(';'.join(MEMCACHE_SERVERS))+"/"


### LEGACY SETUP ###
# these are the settings that seem to be specific to Mamboms


##
## cache middleware settings, these are mamboms specific
##
CACHE_MIDDLEWARE_SECONDS = 5
CACHE_MIDDLEWARE_KEY_PREFIX = "mamboms-"

LOGS = ['mango_ldap', 'mamboms_spectral_search_log', 'mamboms_import_log' ]
TEST_RUNNER = 'mamboms.test.testrunner.run_mamboms_tests'

PERSISTENT_FILESTORE = os.path.normpath(os.path.join(PROJECT_DIRECTORY, '..', '..', 'files')) 
PERSISTENT_FILESTORE_URL = url('/mamboms/files/')

# which directory we put the processed files in
OUTPUT_SUBPATH = "output"
UPLOAD_SUBPATH = "upload"

if not os.path.exists(os.path.join(PERSISTENT_FILESTORE,OUTPUT_SUBPATH)):
    os.mkdir(os.path.join(PERSISTENT_FILESTORE,OUTPUT_SUBPATH))

#Ensure the persistent storage dir exits. If it doesn't, exit noisily.
assert os.path.exists(PERSISTENT_FILESTORE), "This application cannot start: It expects a writeable directory at %s to use as a persistent filestore" % (PERSISTENT_FILESTORE) 


# Load instance settings.
# These are installed locally to this project instance.
# They will be loaded from appsettings.yabiadmin, which can exist anywhere
# in the instance's pythonpath. This is a CCG convention designed to support
# global shared settings among multiple Django projects.
try:
    from appsettings.mamboms import *
except ImportError, e:
    pass