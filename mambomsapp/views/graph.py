from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from mamboms.mambomsapp import models
from mamboms.mambomsapp.graph_cache import cache
from mamboms.mambomsapp.spectra_graph import SpectraGraph
from mamboms.mambomsapp.views.utils import json_encode, json_decode

import decimal

class blankSpectrum():
    def __init__(self):
        pass

def remove_exponent(d):
    return d.quantize(decimal.Decimal(1)) if d==d.to_integral() else d.normalize()

@login_required
def page(request, compound_id):
    '''Passing query string parameters alters how this function works:
       mini=1 will display the minigraph
       spectrumid=1 means the id in the URL is a spectrumID, not a compoundID
    '''
    
    t = "mamboms/graph.html"
    print dict(request.GET)
    if request.GET.get('mini', False):
        t = "mamboms/graph_mini.html"
    if request.GET.get('spectrumid', False):
        spectrum = get_object_or_404(models.Spectrum, pk=compound_id)
        compound = get_object_or_404(models.Compound, pk = spectrum.compound.id)
    else:
        compound = get_object_or_404(models.Compound, pk=compound_id)
        spectrum = blankSpectrum()
        spectrum.id = 0
        print 'spectrumid was false'
    
    '''Return the page containing the graph'''
    return render_to_response(t, {
                "compound" : compound,
                "spectrum" : spectrum,
                "molweight" : remove_exponent(compound.molecular_weight),
           }) 

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
        if req['action'] == 'startImage':
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

