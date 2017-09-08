# Create your views here.
from mamboms import mail_functions

from mamboms.utils import setRequestVars, jsonResponse, json_response, makeJsonFriendly
from mamboms.mambomsapp.views.utils import json_encode
from mamboms import mambomsapp

from django.conf import settings
from django.core.context_processors import csrf
from django.db import transaction

from mamboms.mambomsuser import forms, models


from django.views.decorators.cache import cache_page

from django.contrib.auth.models import User
from mamboms.decorators import authentication_required, admins_only
from django.http import HttpResponseForbidden

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response

import logging
logger = logging.getLogger('mamboms')

# TODO get read of the session and set request vars stuff
# TODO return a JSON error if the user was invalid

@authentication_required
def load_user(request, *args):
    uname = request.REQUEST.get('username', request.user.username)
    try:
        user = User.objects.get(username = uname)
    except User.DoesNotExist:
        logger.debug('Exception: No django user existed with username %s' % (uname))

    # Non-admin users are allowed to load only their details
    if not request.user.profile.is_admin and user != request.user:
        return HttpResponseForbidden

    data = user.profile.get_details()

    setRequestVars(request, success=True, data=data, totalRows=len(data.keys()), authenticated=True, authorized=True)
    return jsonResponse(request, [])

@authentication_required
def save_user(request, *args):
    r = request.POST
    uname = r['originalEmail']
    u = User.objects.get(username = uname)

    # Non-admin users are allowed to save only their details
    if not request.user.profile.is_admin and u != request.user:
        return HttpResponseForbidden

    originalEmail = str(uname)
    password = (str(r.get('password', ''))).strip() #empty password will be ignored anyway.
    #TODO: need error checking on these to prevent users corrupting their userrecord.
    updateDict = {
        'originalEmail': originalEmail, #the username of the user to change
        'username': str(r.get('email', originalEmail)), #if empty, set to originalEmail
        'email': str(r.get('email', originalEmail)), #if empty, set to originalEmail
        'password': password,
        'firstname': str(r.get('firstname', '')),
        'lastname': str(r.get('lastname', '')),
        'telephoneNumber': str(r.get('telephoneNumber', '')),
        'homephone': str(r.get('homephone', '')),
        'physicalDeliveryOfficeName': str(r.get('physicalDeliveryOfficeName', '')),
        'title': str(r.get('title', '')),
        'dept': str(r.get('dept', '')),
        'institute': str(r.get('institute', '')),
        'address': str(r.get('address', '')),
        'supervisor': str(r.get('supervisor', '')),
        'areaOfInterest': str(r.get('areaOfInterest', '')),
        'country': str(r.get('country', ''))
    }

    isAdmin = r.get('isAdmin', 'false')
    isNodeRep = r.get('isNodeRep', 'false')
    isAdmin = (str(isAdmin) in ('true', 'True', '1'))
    isNodeRep = (str(isNodeRep) in ('true', 'True', '1'))

    node = r.get('node', None)
    status = r.get('status', None)
    infoDict = {}   #A dictionary of extra information that the saving process may need *other* than user data.
    infoDict['node'] = node
    infoDict['status'] = status
    infoDict['adminCheckbox'] = isAdmin
    infoDict['noderepCheckbox'] = isNodeRep
    infoDict['password'] = password

    success = False
    try:
        u.profile.save_details(updateDict, infoDict, request.user)
        success = True
    except Exception, e:
        logger.debug('\tException saving details: %s' % (str(e)) )

    if success:
        mail_functions.sendAccountModificationEmail(request, uname)

    nextview = 'admin:usersearch'

    setRequestVars(request, success=success, authenticated=True, authorized=True, mainContentFunction = nextview)
    logger.debug('*** exit ***')

    return jsonResponse(request, [])

@authentication_required
def get_user_info(request):
    user = request.user
    node_id, node = None, None
    if user.profile.node is not None:
        node_id = user.profile.node.id
        node = user.profile.node.name
    response_map = {
        'success': True,
        'username': user.username,
        'fullname': user.profile.full_name,
        'node': node,
        'nodeid': node_id,
        'isAdmin': user.profile.is_admin,
        'isNodeRep': user.profile.is_noderep,
        'isClient': user.profile.is_client
    }
    return HttpResponse(json_encode(response_map))

@admins_only
def list_all_users(request, *args, **kwargs):
    data = models.list_users()
    setRequestVars(request, success=True, items = data, totalRows=len(data), authenticated=True, authorized=True)
    return jsonResponse(request, [])

from django.contrib.auth.decorators import login_required

@authentication_required
@cache_page(60 * 30)
def list_node_users(request):
    usernode = request.user.profile.node

    data = []
    for user in [user for user in User.objects.all() if user.profile.node == usernode]:
        data.append({
            'username': user.username,
            'name': user.profile.full_name,
            'id': user.id
        })
    return json_response(data)


@authentication_required
@cache_page(60 * 30)
def list_users(request):
    ''' Defaults to listing only node users,
        pass ?all=somevalue to list all users
    '''
    if request.GET.get('all', False):
        pool = [user for user in User.objects.all()]
    else:
        usernode = request.user.profile.node
        pool = [user for user in User.objects.all() if user.profile.node == usernode]

    data = []
    for user in pool:
        data.append({
            'username': user.username,
            'name': user.profile.full_name,
            'id': user.id
        })
    return json_response(data)

@authentication_required
def list_all_nodes(request, *args, **kwargs):
    logger.debug('***enter***')
    groups = [
        {'name':'Don\'t Know', 'id':None}
    ]

    group_dicts = models.list_mamboms_nodes()
    for group_dict in group_dicts:
        groups.append( { 'name': group_dict['name'], 'id': group_dict['id'] } )

    setRequestVars(request, success=True, items=groups, totalRows=len(groups), authenticated=True, authorized=True)
    logger.debug('***exit***')

    return jsonResponse(request, [])

def forgot_password(request):
    error = None

    if request.method == "POST":
        form = forms.PasswordResetForm(request.POST)

        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data["username"], email=form.cleaned_data["email"])
                profile = user.profile

                token = profile.generate_password_reset_token()
                profile.password_reset_token = token
                profile.save()

                mail_functions.sendPasswordResetEmail(request, token, user.email)

                return render_to_response("user/forgot_password_sent.html", csrf(request))
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                error = "The username and e-mail address given are not on file. Please check your account details and try again."
        else:
            error = "Please fill out all of the details below."
    else:
        form = forms.PasswordResetForm()

    context = {
        "error": error,
        "form": form,
    }
    context.update(csrf(request))

    return render_to_response("user/forgot_password.html", context)

@transaction.commit_on_success
def reset_password(request):
    if not request.REQUEST.get("token", None):
        return render_to_response("user/reset_password_bad_token.html", csrf(request))

    try:
        profile = models.MambomsLDAPProfile.objects.get(password_reset_token=request.REQUEST["token"])
        user = profile.user
    except (models.MambomsLDAPProfile.DoesNotExist, models.MambomsLDAPProfile.MultipleObjectsReturned):
        return render_to_response("user/reset_password_bad_token.html", csrf(request))

    error = None

    if request.method == "POST":
        form = forms.PasswordChangeForm(request.POST)

        if form.is_valid():
            user.set_password(form.cleaned_data["password"])
            user.save()

            profile.password_reset_token = None
            profile.save()

            return render_to_response("user/reset_password_success.html", csrf(request))
        else:
            error = "Please ensure both passwords are provided and match."
    else:
        form = forms.PasswordChangeForm(initial={
            "token": request.REQUEST["token"],
        })

    context = {
        "error": error,
        "form": form,
    }
    context.update(csrf(request))

    return render_to_response("user/reset_password.html", context)
