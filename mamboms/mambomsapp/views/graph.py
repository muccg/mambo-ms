from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from mamboms.mambomsapp import models
from mamboms.mambomsapp.graph_cache import cache
from mamboms.mambomsapp.spectra_graph import SpectraGraph
from mamboms.mambomsapp.views.utils import json_encode, json_decode


import decimal

def remove_exponent(d):
    return d.quantize(decimal.Decimal(1)) if d==d.to_integral() else d.normalize()

@login_required
def page(request, template="mamboms/graph.html"):
    '''Query string parameters:
       both spectrum_id or compound_id (if there is just one spectrum) are accepted
    '''
    spectrum_id = request.GET.get('spectrum_id')
    compound_id = request.GET.get('compound_id')
    queryvalues = request.GET.get('queryspectra', False)
    if not spectrum_id:
        compound = get_object_or_404(models.Compound, pk = compound_id)
        spectrum = compound.spectrum_set.all()[0]
    else:
        spectrum = get_object_or_404(models.Spectrum, pk = spectrum_id)
    
    '''Return the page containing the graph'''
    templateargs = {
                "compound" : spectrum.compound,
                "spectrum" : spectrum,
                "molweight" : remove_exponent(spectrum.compound.molecular_weight),
           }
    if queryvalues is not False:
        templateargs['queryspectra'] = queryvalues

    return render_to_response(template, templateargs)
@login_required
def page_htt(request):
    return page(request, template="mamboms/graph_htt.html")

@login_required
def image_map(request, spectrum_id):
    '''
    Return the image map for the spectrum.
    This is the bottom image that shows where we zoomed in.
    '''
    # TODO look into caching this in the browser, because the
    # image will change only if the xs and ys of the compound
    # will change
    spectrum = get_object_or_404(models.Spectrum, pk=spectrum_id)
    response = HttpResponse(mimetype='image/png')
    graphmap = SpectraGraph.build_map_graph(spectrum)
    graphmap.write(response)
    return response

@login_required
def start_image(request, spectrum_id):
    spectrum = get_object_or_404(models.Spectrum, pk=spectrum_id)
    graph = SpectraGraph.build_graph(spectrum)
    response = HttpResponse(mimetype='image/png')
    graph.write(response)
    cache.put(graph)
    return response

@login_required
def htt_image(request, compound_id, candidate='', datastart=None, dataend=None):
    if len(candidate) == 0:
        return image(request, spectrum_id)
    
    try:
        #print "candidate was: ", candidate 
        candidate = candidate.split(',')
        if len(candidate) % 2 != 0:
            candidate = candidate[0:-1:]
        candidate = [float(i) for i in candidate]
        #print "candidate is now: ", candidate
    except Exception, e:
        print 'Error interpreting candidate values: %s : %s' % (str(candidate), e)
        return image(request, spectrum_id)
        
    #TODO - integrate this with the cache
    compound = get_object_or_404(models.Compound, pk=compound_id)
    spectrum = compound.spectrum_set.all()[0]
    response = HttpResponse(mimetype='image/png')
    graph = SpectraGraph.build_head_to_tail_graph(spectrum, candidate)
    
    #We don't use the cache for head to tails, because of the queryspectra
    #this logic is from the cache though.
    if datastart is not None and dataend is not None:
            if graph.datastart != datastart or graph.dataend != dataend:
                graph.set_newdatarange(datastart, dataend)
    
    graph.write(response)
    return response

@login_required
def image(request, spectrum_id, datastart, dataend):
    '''
    Return the graph image for the spectrum. 
    This is the main image that shows the section of the graph we zoomed into.
    This will be normally in our cache after the first load, because the request is 
    following an image action request (see below) which caches the graph
    '''
    # TODO move to memcache caching
    spectrum = get_object_or_404(models.Spectrum, pk=spectrum_id)
    response = HttpResponse(mimetype='image/png')
    graph = cache.pop_or_create(spectrum, datastart, dataend)
    graph.write(response)
    cache.put(graph)
    return response

@login_required
def image_action(request):
    '''
    Calculate the new graph image information in response to a user request like
    move to left/right, zoom etc. 
    The graph is put in the cache to avoid re-calculations, as normally a graph_image 
    request (see above) will follow.
    '''
    if (request.method == 'POST'):
        req = json_decode(request.raw_post_data)
        spectrum = get_object_or_404(models.Spectrum, pk=req['spectrumId'])
        # TODO validate JSON ?
        print 'spectrum is', spectrum
        print 'action is', req['action']
        if req['action'] == 'startImage':
            print 'entered startImage'
            graph = SpectraGraph.build_graph(spectrum)
        else:
            graph = cache.pop_or_create(spectrum, req['datastart'], req['dataend'])
            if req['action'] == 'zoom':
                graph.zoom_to(req['newxstart'],req['newxend'])
            elif req['action'] == 'mapzoom':
                graph.mapzoom_to(req['newxstart'],req['newxend'])
            elif req['action'] == 'moveLeft':
                graph.move_left()
            elif req['action'] == 'moveRight':
                graph.move_right() 
               
        imageinfo = graph.to_imageinfo()
        cache.put(graph) 
        return HttpResponse(json_encode(imageinfo))

