from django.http import HttpResponse, HttpResponseForbidden
from ccg.http import HttpResponseUnauthorized

def authentication_required(f):

    def new_function(*args, **kwargs):
        request = args[0] 
        if not request.user.is_authenticated():
            return HttpResponseUnauthorized()
        return f(*args, **kwargs)
    return new_function

def clients_forbidden(f):

    def new_function(*args, **kwargs):
        request = args[0] 
        if not request.user.is_authenticated():
            return HttpResponseUnauthorized()
        if request.user.get_profile().is_client:
            return HttpResponseForbidden()
        return f(*args, **kwargs)
    return new_function

def admins_only(f):

    def new_function(*args, **kwargs):
        request = args[0] 
        if not request.user.is_authenticated():
            return HttpResponseUnauthorized()
        if not request.user.get_profile().is_admin:
            return HttpResponseForbidden()
        return f(*args, **kwargs)
    return new_function

def admins_and_nodereps_only(f):

    def new_function(*args, **kwargs):
        request = args[0] 
        if not request.user.is_authenticated():
            return HttpResponseUnauthorized()
        if not (request.user.get_profile().is_admin or request.user.get_profile().is_noderep):
            return HttpResponseForbidden()
        return f(*args, **kwargs)
    return new_function

