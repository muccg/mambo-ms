import mimetypes, os, posixpath, urllib

from django.http import Http404, HttpResponse
from django.shortcuts import render_mako
from django.contrib.auth.decorators import login_required
from mamboms.decorators import admins_and_nodereps_only
from mamboms.mambomsapp import models
from mamboms import settings
from webhelpers import siteurl

# "Real" view functions 

@admins_and_nodereps_only
def serve_file(request, path):
    root = settings.PERSISTENT_FILESTORE
    path = posixpath.normpath(urllib.unquote(path))
    path = path.lstrip('/') 
    fullpath = os.path.join(root, path)
    if not os.path.isfile(fullpath):
        raise Http404, '"%s" does not exist' % fullpath
    contents = open(fullpath, 'rb').read()
    mimetype = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
    response = HttpResponse(contents, mimetype=mimetype)
    response["Content-Length"] = len(contents)
    return response

@login_required
def frontend(request):
    return render_mako('mamboms/frontend.html',
                APP_SECURE_URL = siteurl(request),
                username = request.user.username
            )

