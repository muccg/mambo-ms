import datetime
from decimal import Decimal
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.db.models import Model
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.db.models import Model

#Json Encoding
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.functional import Promise
from django.utils.translation import force_unicode
from django.utils.encoding import smart_unicode

import logging, logging.handlers
import os
import inspect
from mamboms import settings
class DebugLogger(object):
    '''
        This debug logger registers requests from various python code files 
        to log statements. From the calling code file, you just call:
        
        from utils import debugPrint as dprint
        dprint.register(True, 'somelogfile.log')

        True meaning turn logging on straight away, and the filename being where to log to.
        From now on, the code just calls:

        dprint('*** something ***')

        And the logfile ends up with a line like:

        2009-09-03 14:42:27,802 [utils.py] utils.debugPrint:86 *** something ***

        You can toggle logging on and off (for the current code file) with:
        
        dprint.logging_on()
        dprint.logging_off()

        Passing the optional keyword argument 'all_logging' = True|False
        causes logging to be enabled or disabled globally.
    '''

    def __init__(self):
        self.logging_prefs = {}
        #dict will contain: {'filename' : [logging_enabled, logging_path, logging_object]}
        self.global_on = True

    def logging_on(self, all_logging = False):
        if all_logging:
            self.global_on = True
        else:
            callerfname = inspect.stack()[1][1]
            if self.logging_prefs.has_key(callerfname):
                self.logging_prefs[callerfname][0] = True

    def logging_off(self, all_logging = False):
        if all_logging:
            self.global_on = False
        else:
            callerfname = inspect.stack()[1][1]
            if self.logging_prefs.has_key(callerfname):
                self.logging_prefs[callerfname][0] = False

    def register(self, on, filename=None):
        #first, inspect the caller
        caller = inspect.stack()[1]
        callerfname = caller[1]
        print 'debugprint: regtister, callerfname=', callerfname, 'logging prefs = ', self.logging_prefs
        if not self.logging_prefs.has_key(callerfname):
            self.logging_prefs[callerfname] = [None, None, None, None]
        record = self.logging_prefs[callerfname]
        print 'debugprint: record is', record
        record[0] = on
        
        if filename is not None:
            record[1] = os.path.join(settings.WRITABLE_DIRECTORY, filename)
        else:
            record[1] = None
        
        if record[2] is not None:
            del record[2]
            record[2] = None
        record[2] = logging.getLogger(callerfname) #create a named logger
        record[2].setLevel(logging.DEBUG)
        if record[1] is not None:
            handler = logging.FileHandler(record[1])
        else:
            handler = logging.StreamHandler()
        #handler.setFormatter(logging.Formatter("%(asctime)s [%(filename)s] %(module)s.%(funcName)s:%(lineno)s %(message)s") )
        record[2].addHandler(handler)

        record[3] = '.'.join( callerfname.rsplit('/', 2))

        print 'registered %s' % (callerfname)

    def debugPrint(self, message, thrucall = False):
        #inspect the caller
        if thrucall:
            caller = inspect.stack()[2]
        else:
            caller = inspect.stack()[1]
        callerfname = caller[1]
        if self.global_on and self.logging_prefs.has_key(callerfname) and self.logging_prefs[callerfname][0] == True:
            log = self.logging_prefs[callerfname]
            from time import asctime
            if log is not None:
                log[2].debug('%s [%s](%s:%s) %s ' % (asctime(), log[3], caller[3], caller[2], str(message) ) )
                #log[2].debug(message)
    
    def __call__(self, message, *args, **kwargs):
        self.debugPrint(message, thrucall = True)
            
debugPrint = DebugLogger()

def makeJsonFriendly(data):
    '''
        Will traverse a dict or list compound data struct and
        make any datetime.datetime fields json friendly
    '''
    try:
        if isinstance(data, list):
            for e in data:
                e = makeJsonFriendly(e)
        elif isinstance(data, dict):
            for key in data.keys():
                data[key] = makeJsonFriendly(data[key])
            
        elif isinstance(data, datetime.datetime):
            return str(data)
        else:
            return data #unmodified
    except Exception, e:
        print 'makeJsonFriendly encountered an error: ', str(e)
    return data

# ------------------------------------------------------------------------------
class ModelJSONEncoder(DjangoJSONEncoder):
    """
    (simplejson) DjangoJSONEncoder subclass that knows how to encode fields.y/

    (adated from django.serializers, which, strangely, didn't
     factor out this part of the algorithm)
    """
    def handle_field(self, obj, field):
        return smart_unicode(getattr(obj, field.name), strings_only=True)
    
    def handle_fk_field(self, obj, field):
        related = getattr(obj, field.name)
        if related is not None:
            if field.rel.field_name == related._meta.pk.name:
                # Related to remote object via primary key
                related = related._get_pk_val()
            else:
                # Related to remote object via other field
                related = getattr(related, field.rel.field_name)
        return smart_unicode(related, strings_only=True)
    
    def handle_m2m_field(self, obj, field):
        if field.creates_table:
            return [
                smart_unicode(related._get_pk_val(), strings_only=True)
                for related
                in getattr(obj, field.name).iterator()
                ]
    
    def handle_model(self, obj):
        dic = {}
        for field in obj._meta.local_fields:
            if field.serialize:
                if field.rel is None:
                    dic[field.name] = self.handle_field(obj, field)
                else:
                    dic[field.name] = self.handle_fk_field(obj, field)
        for field in obj._meta.many_to_many:
            if field.serialize:
                dic[field.name] = self.handle_m2m_field(obj, field)
        return dic
    
    def default(self, obj):
        if isinstance(obj, Model):
            return self.handle_model(obj)
        else:
            return super(ModelJSONEncoder, self).default(obj)

# ------------------------------------------------------------------------------
class LazyEncoder(ModelJSONEncoder):
    def default(self, o):
        if isinstance(o, Promise):
            return force_unicode(o)
        else:
            return super(LazyEncoder, self).default(o)


def json_encode(data):
    m = ModelJSONEncoder()
    try:
        d = m.encode(data)
        return d
    except Exception, e:
        print 'json_encode: couldn\'t encode', data, ':', str(e)
        return None

def json_decode(data):
    try:
        m = simplejson.JSONDecoder()
        d = m.decode(data)
        return d
    except Exception, e:
        print 'json_decode: couldn\'t decode ', data, ':', str(e)
        return data



def uniqueList(l):
    '''returns unique elements of l.
       sometimes you can use a set to do this, but 
       not if your list contains unhashable types, such as dict.
    '''
 
    seen = []
    result = []
    for i in l:
        if i not in seen:
            result.append(i)
        seen.append(i)

    return result

# TODO: remove and refactor this
# This is a function for MADAS, which belongs in a MADAS app specific file,
# and can be moved out once MADAS has been refactored to use user_profiles.
def getGroupsForSession(request, force_reload = False):
    cachedgroups = request.session.get('cachedgroups', None)
    if cachedgroups is None or force_reload:
        print '\tNo cached groups for %s. Fetching.' % (request.user.username)
        from mamboms import LDAPHandler
        ld = LDAPHandler()
        g = ld.ldap_get_user_groups(request.user.username)
        request.session['cachedgroups'] = g
        print '\tStored groups for %s: %s' % (request.user.username, request.session.get('cachedgroups') )
        cachedgroups = g
        
        request.session['isNodeRep'] = False
        request.session['isAdmin'] = False
        print 'yes: ', len(cachedgroups), '   ', cachedgroups
        request.session['isClient'] = (len(cachedgroups) == 0)

        for group in cachedgroups:
            if group == 'Administrators':
                request.session['isAdmin'] = True
            if group == 'Node Reps':
                request.session['isNodeRep'] = True

    return cachedgroups 


# TODO:
# This is a function very specific to MA sites that are built with the EXT frontend.
# Consider moving to a MA_Utils file.
def setRequestVars(request, success=False, authenticated = 0, authorized = 0, totalRows = 0, mainContentFunction = '', username='', params = None, items=None, data=None):
    '''
        Make sure we set the session vars the same way each time, with sensible defaults
    '''
    
    if params is None:
        p = request.REQUEST.get('params', None)
        if p is not None:
            p = json_decode(p)
            print '\tSet Request Vars decoded params as : ', p
        params = p
    
    print '\tSet Request Vars params are ', params

    store = {}
    store['success']              = success
    store['authenticated']        = authenticated
    store['authorized']           = authorized
    store['totalRows']            = totalRows
    store['mainContentFunction']  = mainContentFunction
    store['params']               = params
    #print 'Setting params. ', params, 'Type was: ', type(request.store['params'])
    if items is None:
        store['items']            = items
    else:
        store['items']            = list(items)
    #print 'setSessionVars, mainContentFunction is: ', request.store['mainContentFunction'] 
    
    if data is not None:
        store['data'] = data

    #set the store on the session
    request.session['store'] = store

def get_var(dictionary, key, defaultvalue):
    if dictionary.has_key(key):
        v = dictionary[key]
        #if type(v) is list and len(v) ==1:
        #    v = v[0] 
        return v 
    else:
        return defaultvalue


def param_remap(d):
    for key in d:
        if key == 'quoterequestid':
            v = d[key]
            del d[key]
            d['qid'] = v
    return d

# TODO yes, this is named similarly to jsonResponse below, but the idea is to
# slowly move the old code to use a simplified JSON without the unneeded auth
# baggage.
def json_response(data):
    json = {'success': True, 'data': data, 'totalRows': len(data)}
    json = makeJsonFriendly(json)
    return HttpResponse(json_encode(json))

def jsonResponse(request, *args):
    #print 'Using jsonResponse'
    s = request.session.get('store', {} )
    a = {}
    a['success'] =          get_var(s, 'success', False)
    a['totalRows'] =        get_var(s, 'totalRows', 0)
    a['authenticated'] =    get_var(s, 'authenticated', 0)
    a['authorized'] =       get_var(s, 'authorized', 0)
    a['username'] =         request.user.username
    #TODO: This isnt quite right. admin != node rep, node rep != admin


    a['isAdmin'] = request.session.get('isAdmin', False)
    a['isNodeRep'] = request.session.get('isNodeRep', False)
    a['isClient'] = request.session.get('isClient', False)

    #### response 'items' ####    
    resp = {}
    resp['value'] = {}
    i = get_var(s, 'items', None)
    if i is not None:
        #print 'Making friendly: ', i
        #print dir(i)
        makeJsonFriendly(i)

    resp['value']['items'] = i #i 
    resp['value']['total_count'] = a['totalRows']
    resp['value']['version'] = 1 #TODO: work out where this comes from.
    a['response'] = resp 
    ###############################

    ### Data ###
    data = get_var(s, 'data', None) 
    if data is not None:
        a['data'] = makeJsonFriendly(data)


    a['mainContentFunction'] = get_var(s, 'mainContentFunction', '')
    a['params'] = s.get('params', [])
   
    retdata = json_encode(a)
    return HttpResponse(retdata)

