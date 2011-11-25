import mimetypes, os, posixpath, urllib

from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from mamboms.decorators import admins_and_nodereps_only
from mamboms.mambomsapp import models
from mamboms import settings
from ccg.utils import webhelpers
from ccg.utils.webhelpers import siteurl, wsgibase
from django.shortcuts import render_to_response

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

def site_frontend(request):
    print "rendered site_ fe"
    force = request.GET.get('dev_force', False) #param that can be passed to force access to ccg instance, for debugging purposes
    if not force and siteurl(request).find('ccg.murdoch.edu.au') > -1:
        #display the banner
        return render_to_response('mamboms/banner.html',{ 
                'APP_SECURE_URL': siteurl(request), 
                'newurl':'https://mambo.bio21.unimelb.edu.au/mamboms'
                })
    else:
        return frontend(request)

@login_required
def frontend(request):
    print "rendered fe"
    return render_to_response('mamboms/frontend.html', {
                'APP_SECURE_URL': siteurl(request),
                'username':request.user.username
                })

