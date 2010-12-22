from django.contrib.auth.models import User
from django.http import HttpResponse
from mamboms.decorators import authentication_required, clients_forbidden
from mamboms.mambomsapp import models
from django.db.models import Q
from mamboms.mambomsapp.view_models import Compounds_View, PointSet, Spectrum
from mamboms.mambomsapp.views.utils import int_param, decimal_param, json_encode
from mamboms.mambomsapp import dot_product_search
from mamboms.mambomsapp.dot_product_search import SearchAlgorithms
import mamboms.mambomsapp.search_admin_views #this is mainly to make sure the datahash is created


@authentication_required
def keyword_search(request):
    req_params = request.POST
    #for key in req_params.keys():
    #    print '%s: %s' % (key, req_params[key])
    try:
        q = build_search_queryset(req_params, request.user)
        q = sort_queryset(q, req_params)
        start, end = get_range(req_params)
        return HttpResponse(json_encode(mapify_results(q[start:end], q.count())))
    except Exception, e:
        print 'Problem: ', str(e)
        return HttpResponse(json_encode([]) )

def stored_procedure_search(spectra, limit, adjust):
    from django.db import connection
    cursor = connection.cursor()
    try:
        cursor.callproc('search_by_spectra', (",".join(spectra), limit, adjust))
        result = cursor.fetchone()[0]
        return [line.split() for line in result.split('\n') if line]
    except Exception, e:
        print 'Problem running search: ', e
        return []

def dot_product_ma_inhouse(spectra, limit, adjust):
    # TODO search should accept limit as a param
    input = PointSet(','.join(spectra))
    return dot_product_search.search(input, thresh = 0.2, algorithm=SearchAlgorithms.DOTPRODUCT_MA)

def dot_product(spectra, limit, adjust):
    # TODO search should accept limit as a param
    input = PointSet(','.join(spectra))
    return dot_product_search.search(input, thresh = 0.2, algorithm=SearchAlgorithms.DOTPRODUCT)


@clients_forbidden
def spectra_search(request, algorithm=stored_procedure_search):
    req_params = request.POST
    
    print request.POST.keys()
    print request.POST.values()
    
    spectra = req_params['spectra'].split()
    limit = int(req_params['limit'])

    alg_selection = request.POST.get('spectral_algorithm', None)
   
    adjust = 0;
    tokyo = False
    if spectra[len(spectra)-1] == 'tokyo':
        tokyo = True
        spectra.pop()

    if alg_selection is not None:
        alg_selection = int(alg_selection)
        if alg_selection == 1:
            print 'using ma inhouse dot product '
            adjust = 1
            if tokyo:
                algorithm = dot_product_ma_inhouse
        elif alg_selection == 2:
            print 'using normal dot product '
            if tokyo:
                algorithm = dot_product
     
    print 'search by spectra, spectra,limit is:', spectra, limit
    search_result = algorithm(spectra, limit, adjust)
    

    print 'search result: ', search_result

    l = [(score, models.Compound.objects.get(pk=int(id))) for (score,id) in search_result]
    return HttpResponse(json_encode(mapify_scored_compound_results(l, len(l))))

# Implementation 

def build_search_queryset(req_params, user):
    datasets = req_params.getlist('dataset')
    if user.get_profile().is_client:
        # Clients can't search NIST records
        valid_datasets = set(('MA LC', 'MA GC'))
    else:
        valid_datasets = set(('NIST', 'MA LC', 'MA GC'))
    if datasets:
        datasets = set(datasets) & valid_datasets
    else:
        datasets = valid_datasets
    if not datasets:
        return models.Compound.objects.none() # empty queryset

    q = Compounds_View.objects.all()
    #q = models.Compound.objects.all()
    ds = models.Dataset.objects.all()
    ds = ds.filter(name__in = datasets)
    dslist = [d.id for d in ds]
    q = q.filter(dataset__in = dslist)

    def build_clause_for_field(q, field_name, field_value):
        #field_value = req_params.get(field_name)
        if not field_value:
            return {}
        match_type = req_params.get(field_name + '_match_type')
        clause = '__icontains' # default
        if match_type == 'exact':
            clause = '__iexact'
        elif match_type == 'starts with':
            clause = '__istartswith'
        clause_dict = { field_name+clause: field_value }
        print clause_dict
        #q = q.filter(**clause_dict)
        #return q
        return clause_dict

    q1 = build_clause_for_field(q, 'cas_name', req_params.get('compound_name') )
    q2 = build_clause_for_field(q, 'compound_name', req_params.get('compound_name') )
   
    print 'doing compound name filter'
    q = q.filter(Q(**q1) | Q(**q2) )
    print 'finished compound name filter'

    mol_weight_start = decimal_param(req_params, 'mol_weight_start')
    mol_weight_end = decimal_param(req_params, 'mol_weight_end')
    if mol_weight_start:
        q = q.filter(molecular_weight__gte = mol_weight_start)
    if mol_weight_end:
        q = q.filter(molecular_weight__lte = mol_weight_end)
 
    if req_params.get('cas_regno'):
        q = q.filter(cas_regno__iexact = req_params['cas_regno'])
    if req_params.get('mol_formula'):
        q = q.filter(molecular_formula__iexact = req_params['mol_formula'])
   
    if req_params.get('retention_time'):
        q = q.filter(Q(retention_time__iexact = req_params['retention_time'])| Q(retention_time__exact =None) )

    if req_params.get('mono_isotopic_mass'):
        q = q.filter(Q(mono_isotopic_mass__iexact = req_params['mono_isotopic_mass']) | Q(mono_isotopic_mass__exact =None) )

    #Chromatography type is a list
    if req_params.get('chromatography_type'):
        q = q.filter(Q(chromatography_type__in = req_params['chromatography_type'].split(',') ) | Q(chromatography_type__exact =None) )

    #MS Geometry type is a list
    if req_params.get('ms_geometry'):
        q = q.filter(Q(ms_geometry__in = req_params['ms_geometry'].split(',') ) | Q(ms_geometry__exact =None) )

    #Mass Spectra types is a list
    if req_params.get('mass_spectra_types'):
        specs = Spectrum.objects.filter(mass_spectra_type__in = req_params['mass_spectra_types'].split(','))
        cids = [spec.compound.id for spec in specs]

        q = q.filter(Q(id__in = cids))


    #ionization mode is a list
    if req_params.get('ionization_mode'):
        q = q.filter(Q(ionization_mode__in = req_params['ionization_mode'].split(',') ) | Q(ionization_mode__exact =None) )

    #polarity is a list
    if req_params.get('polarity'):
        q = q.filter(Q(polarity__in = req_params['polarity'].split(',') ) | Q(polarity__exact =None) )

    #Biological systems is a list
    if req_params.get('biological_systems'):
        q = q.filter(Q(biological_system__in = req_params['biological_systems'].split(',') ) | Q(biological_system__exact =None) )

    #Metabolite class is a list
    if req_params.get('metabolite_class'):
        q = q.filter(Q(metabolite_class__in = req_params['metabolite_class'].split(',') ) | Q(metabolite_class__exact =None) )

    #Derivitization Agent is a list
    #derivitization agent is a string. Warning: this breaks if they use commas
    #in the freeform name.
    if req_params.get('derivitization_agent'):
        #we have to strip leading/trailing spaces off the names.
        rplist = [s.strip() for s in req_params['derivitization_agent'].split(',')]
        q = q.filter(Q(derivitization_agent__in = rplist ) | Q(derivitization_agent__exact =None) )

    return q

def sort_queryset(q, req_params):
    param_to_column = {'cas_name': 'cas_name', 'node': 'node', 'compound_name': 'compound_name', 
        'cas_regno': 'cas_regno', 'dataset': 'dataset__name',
        'mol_formula': 'molecular_formula', 'mol_weight': 'molecular_weight'}
    orderBy = param_to_column.get(req_params.get('sort'))
    if orderBy:
        if req_params.get('dir', 'ASC') == 'DESC':
            orderBy = "-" + orderBy;
        q = q.order_by(orderBy)
    return q

def get_range(req_params):
    start = int_param(req_params, 'start', 0)
    limit = int_param(req_params, 'limit', 10)
    return (start, start+limit)

def mapify_scored_compound_results(list, total_count):
    json = { 'success': 'true', 'results': total_count, 'data': [] }
    for score,compound in list:
        cmap = mapify_compound(compound)
        cmap['score'] = round(float(score)*100, 2)
        json['data'].append(cmap)
    return json

def mapify_results(q, total_count):
    json = { 'success': 'true', 'results': total_count, 'data': [] }
    for compoundview in q:
        #We convert each compound view item back into its compound.
        #Hopefully we have already LIMITed by this time ;)
        compound = models.Compound.objects.get(id=compoundview.id)
        json['data'].append(mapify_compound(compound))
    return json

def mapify_compound(compound):
    return {
        'id': compound.id, 
        'cas_name': compound.cas_name, 
        'compound_name': compound.compound_name, 
        'node': compound.node.name if compound.node else '',
        'dataset': compound.dataset.name,
        'cas_regno': compound.cas_regno,
        'mol_formula': compound.molecular_formula,
        'mol_weight': str(compound.molecular_weight) if compound.molecular_weight else '',
        'record_uploaded_by': compound.record_uploaded_by.username if compound.record_uploaded_by else ''
    }

