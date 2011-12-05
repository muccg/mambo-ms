from mamboms.mambomsapp.models import Dataset, Compound, PointSet, Spectrum, HashMaintenance
from django.http import HttpResponse
from mamboms.decorators import authentication_required, admins_only, admins_and_nodereps_only
from django.shortcuts import render_to_response, get_object_or_404
from ccg.utils import webhelpers
from ccg.utils.webhelpers import siteurl

import logging
logger = logging.getLogger('mamboms_search_log')

FAST_SEARCH_ENABLED = False
try:
    import search_datastructures as sd
    FAST_SEARCH_ENABLED = True
except:
    pass

def fast_search_disabled():
    return HttpResponse('fast search is not enabled.')

#This is a manual create, if we want to do that
@admins_only
def create_hash(request, qset=None, limit=None, keyspace = 'default'):
    if FAST_SEARCH_ENABLED: 
        sd.low_level_create(keyspace= keyspace)
        return HttpResponse('create done')
    else:
        return fast_search_disabled() 
@admins_only
def build_hash(request, qset = None, limit = None):
    if FAST_SEARCH_ENABLED:
        qset = request.GET.get('qset', None)
        limit = request.GET.get('limit', None)

        if sd.DATAHASH[0] is None or sd.DATAHASH[0].state != sd.DATAHASH[0].STATE_BUILDING:
            logger.debug('building datahash, limit is %s' % (str(limit)) )
            
            #Here, you change your queryset...
            sd.DATAHASH[0].build(Spectrum.objects.all(), limit=limit)
            return HttpResponse('build done')
        else:
            return HttpResponse('build already in progress')
    else:
        return fast_search_disabled()

@admins_only
def update_hash(request):

    if FAST_SEARCH_ENABLED:
        if sd.DATAHASH[0] is None or sd.DATAHASH[0].state != sd.DATAHASH[0].STATE_BUILDING:
            #Here, you change your queryset...
            dirty = HashMaintenance.objects.all()
            dirty_spectrums = Spectrum.objects.filter(id__in=[sp.spectrum.id for sp in dirty])
            sd.DATAHASH[0].build( dirty_spectrums )
            logger.debug('Updating datahash with %d records.' % (dirty.count()) )
            #TODO: there is no proof coming from the build function that all of these were successfully added...
            for d in dirty:
                d.delete()
            
            return HttpResponse('Update done')
        else:
            return HttpResponse('Update or build already in progress')
    else:
        return fast_search_disabled()


@admins_and_nodereps_only
def status(request, *args):
    if FAST_SEARCH_ENABLED:
        if sd.DATAHASH[0] == None:
            return HttpResponse("Not created") 
        d = sd.DATAHASH[0].status(numdirty = HashMaintenance.objects.count())
        #s = ""
        #for k in d.keys():
        #    s += "%s : %s<br>" % (str(k), str(d[k]))
        
        return render_to_response("mamboms/hash_management.html", 
                            stats = d,
                            APP_SECURE_URL = siteurl(request),
                            username = request.user.username)
    else:
        return fast_search_disabled()
    
@admins_only
def clear_hash(request, *args):
    if FAST_SEARCH_ENABLED:
        if sd.DATAHASH[0] is not None:
            sd.DATAHASH[0].clear_hash()
        return HttpResponse('Clear Done')
    else:
        return fast_search_disabled()
