from django.http import HttpResponse
from mamboms.decorators import authentication_required
from mamboms.mambomsapp import models
from mamboms.mambomsapp.views.utils import json_encode, json_decode

@authentication_required
def list_instruments(request):
    if request.GET.get('all', False):
        qs = models.Instrument.objects.all()
    else:
        node = get_node_name(request)
        qs = models.Instrument.objects.filter(node__name=node)

    qs = qs.order_by('name')
    return HttpResponse(json_reference_data(qs))

@authentication_required
def list_biological_systems(request):
    qs = models.BiologicalSystem.objects.all().order_by('kingdom', 'species')
    json = {'success': 'true', 'data': []}
    for bs in qs:
        json['data'].append({
            'id': bs.id,
            'name': "%s - %s" % (bs.kingdom, bs.species)
        })

    return HttpResponse(json_encode(json))

@authentication_required
def list_metabolite_classes(request):
    qs = models.MetaboliteClass.objects.all().order_by('name')
    json = {'success': 'true', 'data': []}
    for mc in qs:
        json['data'].append({
            'id': mc.id,
            'name': mc.name
        })

    return HttpResponse(json_encode(json))

@authentication_required
def list_ionized_species(request):
    qs = models.LCModification.objects.all().order_by('name_of_compound')
    json = {'success': 'true', 'data': []}
    for lcm in qs:
        json['data'].append({
            'id': lcm.id,
            'name': lcm.name_of_compound
        })

    return HttpResponse(json_encode(json))

@authentication_required
def list_chromatography_types(request):
    qs = models.ChromatographyType.objects.all().order_by('name')
    json = {'success': 'true', 'data': []}
    for ct in qs:
        json['data'].append({
            'id': ct.id,
            'name': ct.name
        })
    return HttpResponse(json_encode(json))

@authentication_required
def list_ms_geometry_types(request):
    qs = models.MSGeometry.objects.all().order_by('name')
    json = {'success': 'true', 'data': []}
    for gt in qs:
        json['data'].append({
            'id': gt.id,
            'name': gt.name
        })
    return HttpResponse(json_encode(json))
    
@authentication_required
def list_ionization_modes(request):
    qs = models.IonizationMode.objects.all().order_by('name')
    json = {'success': 'true', 'data': []}
    for im in qs:
        json['data'].append({
            'id': im.id,
            'name': im.name
        })
    return HttpResponse(json_encode(json))

@authentication_required
def list_polarities(request):
    qs = dict(models.MethodBase.POLARITY_CHOICES)
    json = {'success': 'true', 'data': []}
    for polarityid in qs.keys():
        json['data'].append({
            'id': polarityid,
            'name': qs[polarityid]
        })
    return HttpResponse(json_encode(json))



@authentication_required
def list_lcmethods(request, bynode=False):
    node = get_node_name(request)
    if bynode:
        qs = models.LCMethod.objects.filter(node__name = node).order_by('name')
    else:
        qs = models.LCMethod.objects.all().order_by('name')
    json = {'success': 'true', 'data': []}
    for m in qs:
        json['data'].append({
                'id': m.id,
                'name': m.name,
                'platform': m.platform,
                'deriv_agent': m.derivitization_agent,
                'mz_adducts': m.mz_exp_deriv_adducts,
                'mass_range': m.mass_range_acquired,
                'instrument_method': file_field_to_url(m.instrument_method),
                'method_summary': file_field_to_url(m.method_summary),
                'polarity': dict(models.LCMethod.POLARITY_CHOICES)[m.polarity],
                'ionization_mode': m.ionization_mode.name
            })
    return HttpResponse(json_encode(json))

@authentication_required

def list_derivitization_agents(request):
    node = get_node_name(request)
    json = {'success': 'true', 'data': []}
    data = []
    
    #get the LC
    qs = models.LCMethod.objects.all().order_by('name')
    for m in qs:
        da = m.derivitization_agent
        if da not in data:
            data.append(da)
    #get the GC
    qs = models.GCMethod.objects.all().order_by('name')
    for m in qs:
        da = m.derivitization_agent
        if da not in data:
            data.append(da)
    
    for entry in data:
        json['data'].append({'name' : entry})

    return HttpResponse(json_encode(json))

@authentication_required
def list_gcmethods(request, bynode="false"):
    print 'bynode was: ', bynode
    node = get_node_name(request)
    if bynode is not "false":
        qs = models.GCMethod.objects.filter(node__name = node).order_by('name')
    else:
        qs = models.GCMethod.objects.all().order_by('name')
    json = {'success': 'true', 'data': []}
    for m in qs:
        json['data'].append({
                'id': m.id,
                'name': m.name,
                'platform': m.platform,
                'deriv_agent': m.derivitization_agent,
                'mass_adducts': m.mass_exp_deriv_adducts,
                'mass_range': m.mass_range_acquired,
                'instrument_method': file_field_to_url(m.instrument_method),
                'method_summary': file_field_to_url(m.method_summary)
            })
    return HttpResponse(json_encode(json))

@authentication_required
def list_columns(request):
    if request.GET.get('all', False):
        qs = models.Column.objects.all()
    else:
        node = get_node_name(request)
        qs = models.Column.objects.filter(node__name=node)
    qs = qs.order_by('name', 'length', 'dimension')
    json = {'success': 'true', 'data': []}
    for c in qs:
        json['data'].append({
                'id': c.id,
                'name': "%s - %s - %s" % (c.name, c.length, c.dimension)
            })
 
    return HttpResponse(json_encode(json))

@authentication_required
def list_precursor_selections(request):
    qs = models.PrecursorSelection.objects.all()
    json = {'success': 'true', 'data': []}
    for presel in qs:
        json['data'].append({
                'id': presel.id,
                'name': presel.name
            })

    return HttpResponse(json_encode(json))

@authentication_required
def list_precursor_types(request):
    qs = models.PrecursorType.objects.all()
    json = {'success': 'true', 'data': {'P': [], 'N': []}}
    for pretype in qs:
        polarity = json['data'][pretype.polarity]
        polarity.append({
                'id': pretype.id,
                'name': pretype.name
            })

    return HttpResponse(json_encode(json))

@authentication_required
def list_mass_spectra_types(request):
    qs = models.MassSpectraType.objects.all()
    json = {'success': 'true', 'data': []}
    for mst in qs:
        json['data'].append({
                'id': mst.id,
                'name': mst.name
            })
    return HttpResponse(json_encode(json))

# Implementation 

def file_field_to_url(field):
    url = 'N/A'
    if field.name:
        url = '<a href="%s" target="_blank">%s</a>' % (field.url, field.name)
    return url

def json_reference_data(qs):
    json = {'success': 'true', 'data': []}
    for ref_data in qs:
        json['data'].append({
                'id': ref_data.id,
                'name': ref_data.name
            })
    return json_encode(json)

def get_node_name(request):
    node = request.user.get_profile().node
    return None if node is None else node.name



