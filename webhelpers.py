#!/usr/bin/env python

"""Some web helpers taken from the Pylons camp"""

import os
import settings

basejs="javascript"
basecss="css"
wsgibasepath=os.environ['SCRIPT_NAME']

def javascript_include_tag( jsfile ):
	# make sure the filename ends with .js
	jsfile = "%s.js"%jsfile if not jsfile.endswith(".js") else jsfile

	jspath=wsgibasepath+"/"+"/".join([basejs,jsfile])
	return '<script src="%s" type="text/javascript"></script>'%jspath

def stylesheet_link_tag( stylefile ):
	csspath=wsgibasepath+"/"+"/".join([basecss,stylefile])
	return '<link rel="stylesheet" type="text/css" href="%s">'%csspath

def wsgibase():
	return wsgibasepath

def url( relpath ):
	if relpath[0]=='/' and len(wsgibasepath):
		return "%s%s"%(wsgibasepath,relpath)
	return relpath

