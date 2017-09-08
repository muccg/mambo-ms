from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from mamboms.mambomsapp.models import Compound
from mamboms.mambomsapp.spectra_graph import SpectraGraph
from mamboms.mambomsapp.graph_cache import cache
from django.conf import settings
import logging
import os
logger = logging.getLogger('mamboms')

def graph(request, compound_id):
    compound = get_object_or_404(Compound, pk=compound_id)
    return render_to_response("mamboms/graph.html", {
                "compound" : compound,
           })

def graph_image(request, compound_id, datastart, dataend):
    compound = get_object_or_404(Compound, pk=compound_id)
    response = HttpResponse(mimetype='image/png')
    graph = cache.pop_or_create(compound, datastart, dataend)
    graph.write(response)
    cache.put(graph)
    return response

def graph_image_action(request):
    if (request.method == 'POST'):
        decoder = simplejson.JSONDecoder()
        encoder = simplejson.JSONEncoder()
        req = decoder.decode(request.raw_post_data)
        compound = get_object_or_404(Compound, pk=req['compoundId'])
        # TODO validate JSON ?
        if req['action'] == 'startImage':
            graph = SpectraGraph(compound)
        else:
            graph = cache.pop_or_create(compound, req['datastart'], req['dataend'])
            if req['action'] == 'zoom':
                graph.zoom_to(req['newxstart'],req['newxend'])
            elif req['action'] == 'moveLeft':
                graph.move_left()
            elif req['action'] == 'moveRight':
                graph.move_right()

        imageinfo = graph.to_imageinfo()
        cache.put(graph)
        return HttpResponse(encoder.encode(imageinfo))


####################################
# This is the weighting algotithm,
# implemented in numpy for efficiency.
#
# The intensity and mass powers can
# be made configurable.
#
def w_N(specimen):
    import numpy as np
    pow_intensity = 0.5
    pow_mass = 3

    ints = specimen[1]**pow_intensity
    masses = specimen[0]**pow_mass

    return ints * masses

#####################################
# This is the dot product algorithm,
# implemented in numpy for efficiency.
#
# u = unknown sample
# l = library sample

def dot_product_N(u, l, fn):
    import numpy as np
    udata = np.array([u.xs,u.ys]) #construct numpy array from unknown x's and y's
    ldata = np.array([l.xs,l.ys]) #construct numpy array from library x's and y's

    logger.debug('numpy version(l): %s' % (str(ldata[0])) ) #debug message
    logger.debug('numpy version(u): %s' % (str(udata[0])) ) #debug message

    common_masses = np.intersect1d(ldata[0], udata[0])  #find the intersection of masses
    logger.debug('Common masses: %s'%(str(common_masses)) )   #debug message

    #build lists containing each common mass and the corrosponding intensity.
    #We cannot use numpy for this, so we use standard python lists
    '''
    #approach 1:
    ly = []
    uy = []
    for m in common_masses:
        count = 0
        for mass in ldata[0]:
            if m == mass:
                ly.append(ldata[1][count])
            count += 1
        count = 0
        for mass in udata[0]:
            if m == mass:
                uy.append(udata[1][count])
            count += 1
    '''
    #approach 2: list comprehensions.
    #relies on values in common masses being unique, which they are.
    ly = [ldata[1][i] for i in range(len(ldata[0])) if ldata[0][i] in common_masses ]
    uy = [udata[1][i] for i in range(len(udata[0])) if udata[0][i] in common_masses ]

    #now we have data we can feed to the function
    lfndata = np.array([common_masses, ly])
    ufndata = np.array([common_masses, uy])

    #calculate fn result for l and u
    #this should be an array of numbers, one for each mass in the original
    lfn_result = fn(lfndata)
    ufn_result = fn(ufndata)

    lr2 = lfn_result**2 #lr2 = lfnresult squared
    ur2 = ufn_result**2 #ur2 = ufnresult squared

    #top is the sum of the results multiplied
    top = np.sum(lfn_result * ufn_result)
    #bottom is each squared term sum sqrted and multiplied together
    bottom = np.sum(lr2)**0.5 * np.sum(ur2)**0.5

    #avoid a divide by zero, and return early if either term is 0
    if bottom == 0.0 or top==0.0:
        return 0.0

    answer = (top)/bottom

    return answer

def dotsearchTest(request, id=0, num=0):
    import time
    t = time.time()
    l = Compound.objects.get(id = id)

    u = Compound.objects.all()[:num]
    logger.debug('Beginning dot search: %s against %s compounds' % (str(id), str(num)) )

    resultstr = ""
    resultstr += "Reference: %s<br>" % (l.link_to_graph())
    count = 0
    results_list = []
    for sample in u:
        #print count
        count += 1
        results_list.append( (dot_product_N(l, sample, w_N), sample.link_to_graph()) )

    results_list.sort(cmp=lambda x,y: int(x[0]*100000-y[0]*100000) ) #sort on the 0th element of each tuple

    count = 0
    for r in results_list:
        count += 1
        resultstr += "%d: %f : %s<br>" % (count, r[0], r[1])


    t2 = time.time()
    logger.debug('Time was: %s' %(str(t2-t)))
    return HttpResponse('Done.<br>%s' % resultstr)

def dotsearchJSON(request, id=0, num=0, pagenum=1):
    id = int(id)         #the id of the unknown compound
    num = int(num)       #how many records we are comparing 'per page'
    pagenum=int(pagenum) #which page we are up to
    if pagenum < 1:
        pagenum = 1
    import time
    t = time.time()
    u = Compound.objects.get(id = id)

    l = Compound.objects.all()[num*(pagenum-1):num*pagenum] #paginate the compound list

    logger.debug('Beginning dot search: %s against %s compounds' % (str(id), str(num)) )

    resultstr = ""
    resultstr += "Reference: %s<br>" % (u.link_to_graph())
    count = 0
    results_list = []

    #For each sample, run the dot product against u, using a weighting function w
    for sample in l:
        count += 1
        #the weighting function used is w_N - the numpy version of w
        results_list.append( (dot_product_N(u, sample, w_N), sample.truncated_name(), sample.link_to_graph() ) )

    results_list.sort(cmp=lambda x,y: int(x[0]*100000-y[0]*100000) ) #sort on the 0th element of each tuple

    t2 = time.time()
    logger.debug('Time was: %s' %(str(t2-t)))
    a = simplejson.dumps(results_list)
    logger.debug('JSON is : %s' % (str(a)) )
    return HttpResponse(a)

def dotsearchMain(request, id=0, num=0):
    comp = Compound.objects.get(id=id)
    from ccg_django_utils import webhelpers
    return render_to_response("mamboms/dotsearch.html",
                            {
                                "compoundid" : id,
                                "compoundname" : comp.name,
                                "compoundgraph" : comp.link_to_graph(),
                                "perpage" : num,
                                "urlbase" : webhelpers.url('/mamboms/search/dotsearchjson/'),
                            })





