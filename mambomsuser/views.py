# Create your views here.
from mamboms import LDAPHandler

from mamboms.utils import setRequestVars, jsonResponse, json_response, makeJsonFriendly
from mamboms.mambomsapp.views.utils import json_encode
from mamboms import mambomsapp

from django.conf import settings

from mamboms.mambomsuser import models


from django.views.decorators.cache import cache_page

from django.contrib.auth.models import User
from mamboms.decorators import authentication_required, admins_only
from django.http import HttpResponseForbidden

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from mamboms.utils import debugPrint as dprint
dprint.register(True)

# TODO get read of the session and set request vars stuff
# TODO return a JSON error if the user was invalid

@authentication_required
def load_user(request, *args):
    uname = request.REQUEST.get('username', request.user.username)
    try:
        user = User.objects.get(username = uname)
    except User.DoesNotExist:
        dprint('Exception: No django user existed with username %s' % (uname))

    # Non-admin users are allowed to load only their details
    if not request.user.get_profile().is_admin and user != request.user:
        return HttpResponseForbidden

    data = user.get_profile().get_details()

    setRequestVars(request, success=True, data=data, totalRows=len(data.keys()), authenticated=True, authorized=True)
    return jsonResponse(request, [])

@authentication_required
def save_user(request, *args):
    r = request.REQUEST
    uname = r['originalEmail'] 
    u = User.objects.get(username = uname)

    # Non-admin users are allowed to save only their details
    if not request.user.get_profile().is_admin and u != request.user:
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
        u.get_profile().save_details(updateDict, infoDict, request.user)
        success = True
    except Exception, e:
        dprint('\tException saving details: %s' % (str(e)) )
    
    if success:
        from mail_functions import sendAccountModificationEmail
        sendAccountModificationEmail(request, uname)

    nextview = 'admin:usersearch'

    setRequestVars(request, success=True, authenticated=True, authorized=True, mainContentFunction = nextview)
    dprint('*** exit ***')

    return jsonResponse(request, []) 

@authentication_required
def get_user_info(request):
    user = request.user
    node_id, node = None, None
    if user.get_profile().node is not None:
        node_id = user.get_profile().node.id
        node = user.get_profile().node.name
    response_map = {
        'success': True,
        'username': user.username,
        'fullname': user.get_profile().full_name,
        'node': node,
        'nodeid': node_id,
        'isAdmin': user.get_profile().is_admin,
        'isNodeRep': user.get_profile().is_noderep,
        'isClient': user.get_profile().is_client
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
    usernode = request.user.get_profile().node

    data = []
    for user in [user for user in User.objects.all() if user.get_profile().node == usernode]:
        data.append({
            'username': user.username,
            'name': user.get_profile().full_name
        })
    return json_response(data)

@authentication_required
def list_all_nodes(request, *args, **kwargs):
    dprint('***enter***')
    groups = [
        {'name':'Don\'t Know', 'submitValue':''} 
    ]

    group_names = models.list_mamboms_nodes()
    for group_name in group_names:
        groups.append( { 'name': group_name, 'submitValue': group_name } )

    setRequestVars(request, success=True, items=groups, totalRows=len(groups), authenticated=True, authorized=True)
    dprint('***exit***')

    return jsonResponse(request, [])
