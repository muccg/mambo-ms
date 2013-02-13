#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

#
# WSGI bootstrapper for django project ${ project_name }
#

# settings for project
VIRTUAL_PYTHON = True

# where are we installed
PROJECT_DIR = os.path.dirname(__file__)            # project/nutrition
PROJECT_PARENT_DIR = os.path.dirname(PROJECT_DIR)           # project/

if VIRTUAL_PYTHON:
    # virtual python env setup
    import site
    site.addsitedir(os.path.join(PROJECT_DIR,"virtualpython","lib","python2.6","site-packages"))
    site.addsitedir(PROJECT_DIR)

# the parent directory to search
sys.path.append(PROJECT_DIR)
sys.path.append(PROJECT_PARENT_DIR)
sys.path.append(os.path.join("/usr","local","etc","ccgapps"))
# Reverse sys.path so that virtualpython libraries override base python ones.
sys.path.reverse()

print sys.path

# save the project dir in a environment variable
os.environ['PROJECT_DIRECTORY']=PROJECT_DIR

# set up the egg cache
eggdir = os.path.join(PROJECT_DIR,"scratch","egg-cache")
try:
    os.makedirs(eggdir)
except OSError, ose:
    pass
os.environ['PYTHON_EGG_CACHE']=eggdir

# matplot lib needs a writable configuration area
eggdir = os.path.join(PROJECT_DIR,"scratch","matplotlib-conf")
try:
    os.makedirs(eggdir)
except OSError, ose:
    pass
os.environ['MPLCONFIGDIR']=eggdir


# setup the settings module for the WSGI app
os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings'%(os.path.basename(PROJECT_DIR))

import django.core.handlers.wsgi

# This is the WSGI application booter
def application(environ, start):
    os.environ['SCRIPT_NAME']=environ['SCRIPT_NAME']
    if 'DJANGODEV' in environ:
        os.environ['DJANGODEV']=environ['DJANGODEV']
    return django.core.handlers.wsgi.WSGIHandler()(environ,start)
