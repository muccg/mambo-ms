import decimal, os, re 

from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.db import transaction
from mamboms.mambomsapp import models
from django.contrib.auth.models import User
from mamboms.decorators import authentication_required
from mamboms.mambomsapp.views.utils import json_encode

@authentication_required
def delete(request):
    id = int(request.REQUEST.get('id'))
    try:
        compound = get_object_or_404(models.Compound,id=id)
        compound.delete_by(request.user)
        return HttpResponse(json_encode({'success': True, 'id': id}))
    except models.NotAuthorizedError:
        return HttpResponseForbidden()

@authentication_required
def vet(request):
    id = int(request.REQUEST.get('id'))
    compound = get_object_or_404(models.Compound,id=id) 
    try:
        compound.vet(request.user)
        return HttpResponse(vetted_by(compound))
    except models.NotAuthorizedError:
        return HttpResponseForbidden()
    
@authentication_required
@transaction.commit_on_success
def save_lc(request):
    req = request.POST
    profile = request.user.get_profile()
    if not (profile.is_admin or profile.is_noderep):
        return HttpResponseForbidden()

    # TODO it would be probably nicer if we had separate views for insert and update

    id = req.get('id')
    if id:
        lc_rec = get_object_or_404(models.LCMARecord,id=id) 
        if lc_rec.record_uploaded_by != request.user:
            return HttpResponseForbidden()
    else:
        lc_rec = models.LCMARecord()

    errors = validate_metabolite(req)
    if errors:
        json = {'success': False, 'errors': {} }
        for k in errors:
            json['errors'][k] = errors[k]
        return HttpResponse(json_encode(json))

    
    lc_rec.known = req.get('known', 'false') == 'true'
    instrument_id = int(req.get('instrument', '-1'))
    lc_rec.instrument = models.Instrument.objects.get(pk=instrument_id)
    method_id = int(req.get('method', '-1'))
    lc_rec.method = models.LCMethod.objects.get(pk=method_id)
    column_id = int(req.get('column', '-1'))
    lc_rec.column = models.Column.objects.get(pk=column_id)
    sample_run_by = req.get('sample_run_by')
    if sample_run_by is not None:
        lc_rec.sample_run_by = User.objects.get(username=sample_run_by) 
    if not lc_rec.id:
        lc_rec.dataset = models.Dataset.objects.get(name='MA LC')
        lc_rec.node = models.Node.objects.get(name=request.user.get_profile().node)
        lc_rec.record_uploaded_by = request.user
    lc_rec.compound_name = req.get('compound_name')
    biosys_ids = req.getlist('biological_systems')
    metabolite_class_id = int(req.get('metabolite_class', '-1'))
    lc_rec.metabolite_class = models.MetaboliteClass.objects.get(pk=metabolite_class_id)
    lc_rec.cas_name = req.get('cas_name')
    lc_rec.cas_regno = req.get('cas_regno')
    lc_rec.molecular_formula = req.get('mol_formula')
    print 'mol weight is: ', req.get('mol_weight')
    lc_rec.molecular_weight = decimal.Decimal(req.get('mol_weight'))
    #Google Code issue #40 - Ionized Species is a LC Modifications
    #ionized species can come back as '', since we specified tha
    #it was optional in the form js.
    ionized_species = req.get('ionized_species', '')
    if len(ionized_species) == 0:
        ionized_species = -1
    ionized_species = int(ionized_species)
    if ionized_species is not -1:
        lc_rec.ionized_species = models.LCModification.objects.get(pk=ionized_species)
    else:
        lc_rec.ionized_species = None
    
    lc_rec.mono_isotopic_mass = decimal.Decimal(req.get('mono_isotopic_mass'))
    lc_rec.retention_time = req.get('retention_time')
    lc_rec.retention_index = req.get('retention_index')
    lc_rec.kegg_id = req.get('kegg_id')
    lc_rec.kegg_link = req.get('kegg_link')
    lc_rec.extract_description = req.get('extract_description')
    lc_rec.save() 

    structure = request.FILES.get('structure')
    if structure:
        lc_rec.structure.save(structure.name, structure, save=True)

    lc_rec.synonyms.all().delete()
    for syn in [ s.strip() for s in req.get('synonyms', '').split(',') ]:
        lc_rec.synonyms.add(models.Synonym(name=syn))

    biosys_id_list = set([int(s) for s in biosys_ids if s])
    for bs in lc_rec.biological_systems.all(): 
        lc_rec.biological_systems.remove(bs)
    for biosys_id in biosys_id_list:
        bs = models.BiologicalSystem.objects.get(pk=biosys_id)
        lc_rec.biological_systems.add(bs)

    def save_spectrum(prefix, request):
        id = request.get(prefix + '_id')
        if id:
            spectrum = models.Spectrum.objects.get(id=id)
        else:
            spectrum = models.Spectrum()
            
        mass_spectra_type_id = int(request.get(prefix + '_mass_spectra_type', '-1'))
        spectrum.mass_spectra_type = models.MassSpectraType.objects.get(pk=mass_spectra_type_id)
        spectrum.description = request.get(prefix + '_description')
        precursor_type_id = int(request.get(prefix + '_precursor_type', '-1'))
        spectrum.precursor_type = models.PrecursorType.objects.get(pk=precursor_type_id)
        precursor_selection_id = int(request.get(prefix + '_precursor_selection', '-1'))
        spectrum.precursor_selection = models.PrecursorSelection.objects.get(pk=precursor_selection_id)
        spectrum.collison_energy = request.get(prefix + '_collison_energy')
        csv_points = ",".join(request.get(prefix + '_mass_spectra').split())
        spectrum.raw_points = csv_points
        lc_rec.spectrum_set.add(spectrum)

    def extract_spectrum_prefixes(request):
        spec = re.compile(r'(?P<prefix>spectrum\d+)_')
        return set( [spec.match(param).group('prefix') for param in req if spec.match(param) ])
    
    prefixes = extract_spectrum_prefixes(request)
    to_be_updated = [int(req.get(prefix + '_id')) for prefix in prefixes if req.get(prefix + '_id')]
    for spectra in lc_rec.spectrum_set.all():
        if spectra.id not in to_be_updated:
            spectra.delete()
    for prefix in prefixes:
        save_spectrum(prefix, req)
    
    json = {'success': True, 'id': lc_rec.id}
    return HttpResponse(json_encode(json))

@authentication_required
@transaction.commit_on_success
def save(request):
    req = request.REQUEST
    profile = request.user.get_profile()
    if not (profile.is_admin or profile.is_noderep):
        return HttpResponseForbidden()

    # TODO it would be probably nicer if we had separate views for insert and update

    id = req.get('id')
    if id:
        gc_rec = get_object_or_404(models.GCMARecord,id=id) 
        if gc_rec.record_uploaded_by != request.user:
            return HttpResponseForbidden()
    else:
        gc_rec = models.GCMARecord()

    errors = validate_metabolite(req)
    if errors:
        json = {'success': False, 'errors': {} }
        for k in errors:
            json['errors'][k] = errors[k]
        return HttpResponse(json_encode(json))

    gc_rec.known = req.get('known', 'false') == 'true'
    instrument_id = int(req.get('instrument', '-1'))
    gc_rec.instrument = models.Instrument.objects.get(pk=instrument_id)
    method_id = int(req.get('method', '-1'))
    gc_rec.method = models.GCMethod.objects.get(pk=method_id)
    column_id = int(req.get('column', '-1'))
    gc_rec.column = models.Column.objects.get(pk=column_id)
    sample_run_by = req.get('sample_run_by')
    if sample_run_by is not None:
        gc_rec.sample_run_by = User.objects.get(username=sample_run_by) 
    if not gc_rec.id:
        gc_rec.dataset = models.Dataset.objects.get(name='MA GC')
        gc_rec.node = models.Node.objects.get(name=request.user.get_profile().node)
        gc_rec.record_uploaded_by = request.user
    gc_rec.compound_name = req.get('compound_name')
    biosys_ids = req.getlist('biological_systems')
    metabolite_class_id = int(req.get('metabolite_class', '-1'))
    gc_rec.metabolite_class = models.MetaboliteClass.objects.get(pk=metabolite_class_id)
    gc_rec.cas_name = req.get('cas_name')
    gc_rec.cas_regno = req.get('cas_regno')
    gc_rec.molecular_formula = req.get('mol_formula')
    print 'GC mol weight is: ', req.get('mol_weight')
    gc_rec.molecular_weight = decimal.Decimal(req.get('mol_weight'))
    gc_rec.retention_time = req.get('retention_time')
    gc_rec.retention_index = req.get('retention_index')
    gc_rec.kegg_id = req.get('kegg_id')
    gc_rec.kegg_link = req.get('kegg_link')
    csv_points = ",".join(req.get('mass_spectra').split())
    get_optional_decimal = lambda n: decimal.Decimal(req.get(n)) if req.get(n) and req.get(n) != 'Enter value with decimals' else None
    gc_rec.quant_ion = get_optional_decimal('quant_ion')
    gc_rec.qualifying_ion_1 = get_optional_decimal('qual_ion_1')
    gc_rec.qualifying_ion_2 = get_optional_decimal('qual_ion_2')
    gc_rec.qualifying_ion_3 = get_optional_decimal('qual_ion_3')
    gc_rec.extract_description = req.get('extract_description')
    gc_rec.save() 

    structure = request.FILES.get('structure')
    if structure:
        gc_rec.structure.save(structure.name, structure, save=True)

    gc_rec.synonyms.all().delete()
    for syn in [ s.strip() for s in req.get('synonyms', '').split(',') ]:
        gc_rec.synonyms.add(models.Synonym(name=syn))

    if gc_rec.spectrum_set.all():
        spectrum = gc_rec.spectrum_set.all()[0]
    else:
        spectrum = models.Spectrum()
    spectrum.raw_points = csv_points
    if spectrum.pk:
        spectrum.save()
    else:
        gc_rec.spectrum_set.add(spectrum)

    biosys_id_list = set([int(s) for s in biosys_ids if s])
    for bs in gc_rec.biological_systems.all(): 
        gc_rec.biological_systems.remove(bs)
    for biosys_id in biosys_id_list:
        bs = models.BiologicalSystem.objects.get(pk=biosys_id)
        gc_rec.biological_systems.add(bs)

    json = {'success': True, 'id': gc_rec.id}
    return HttpResponse(json_encode(json))

@authentication_required
def gcmetabolite_load(request):
    return GCLoader().load(request)

@authentication_required
def lcmetabolite_load(request):
    return LCLoader().load(request)

# Implementation

class CompoundLoader(object):
    def load(self, request):
        id = int(request.GET.get('id'))
        self.compound = get_object_or_404(self.compound_class,id=id) 
        self.user = request.user
       
        json = {'success': True}
        json['data'] = self.jsonify(self.compound)
    
        return HttpResponse(json_encode(json))

    def biological_systems_ids(self):
        return ",".join([str(bs.pk) for bs in self.compound.biological_systems.all()])

    def jsonify(self, gc_rec):
        data = {
            # I don't like this, but readonly CSS disabled fields get rendered incorrectly in IE
            # and disabled text boxes aren't submitted, so we have one id for display and a hidden
            # field for submit
            'id': gc_rec.id,
            'id_display': gc_rec.id,
            'known': gc_rec.known,
            'node': gc_rec.node.name,
            'instrument': gc_rec.instrument_id,
            'method': gc_rec.method.id,
            'platform': gc_rec.method.platform,
            'deriv_agent': gc_rec.method.derivitization_agent,
            'mass_range': gc_rec.method.mass_range_acquired,
            'instrument_method': file_field_to_url(gc_rec.method.instrument_method),
            'method_summary': file_field_to_url(gc_rec.method.method_summary),
            'column': gc_rec.column_id,
            'sample_run_by': gc_rec.sample_run_by.username,
            'uploaded_by': gc_rec.record_uploaded_by.get_profile().full_name,
            'uploaded_date': str(gc_rec.record_uploaded_on),
            'vetted_by': vetted_by(gc_rec),
            'can_vet': gc_rec.can_be_vetted_by(self.user),
            'compound_name': gc_rec.compound_name,
            'synonyms': ",".join([syn.name for syn in gc_rec.synonyms.all().order_by('name')]),
            'biological_systems': self.biological_systems_ids(),
            'metabolite_class': gc_rec.metabolite_class_id,
            'cas_name': gc_rec.cas_name,
            'cas_regno': gc_rec.cas_regno,
            'mol_formula': gc_rec.molecular_formula,
            'mol_weight': str(gc_rec.molecular_weight),
            'retention_time': gc_rec.retention_time,
            'retention_index': gc_rec.retention_index,
            'kegg_id': gc_rec.kegg_id,
            'kegg_link': gc_rec.kegg_link,
            'extract_description': gc_rec.extract_description,
            'structure': os.path.basename(gc_rec.structure.name) if gc_rec.structure.name else None
        }
        data.update(self.additional_fields())
        return data
        
class GCLoader(CompoundLoader):
    def __init__(self):
        self.compound_class = models.GCMARecord     

    def additional_fields(self):
        gc_rec = self.compound
        return {
            'mass_adducts':gc_rec.method.mass_exp_deriv_adducts,
            'mass_spectra': format_mass_spectra(gc_rec.point_set),
            'quant_ion': str(gc_rec.quant_ion),
            'qual_ion_1': str(gc_rec.qualifying_ion_1),
            'qual_ion_2': str(gc_rec.qualifying_ion_2),
            'qual_ion_3': str(gc_rec.qualifying_ion_3),
            'qual_ion_ratio_1_2': "%.3f" % gc_rec.qualifying_ion_ratio12 if gc_rec.qualifying_ion_ratio12 is not None else 'N/A',
            'qual_ion_ratio_2_3': "%.3f" % gc_rec.qualifying_ion_ratio23 if gc_rec.qualifying_ion_ratio23 is not None else 'N/A'
        }

class LCLoader(CompoundLoader):
    def __init__(self):
        self.compound_class = models.LCMARecord

    def additional_fields(self):
        lc_rec = self.compound
        data = {
            'mass_adducts':lc_rec.method.mz_exp_deriv_adducts,
            'mono_isotopic_mass': str(lc_rec.mono_isotopic_mass),            
            'spectrum_count': lc_rec.spectrum_set.count(),
            'ionized_species': lc_rec.ionized_species_id,
        }

        for i, spectrum in enumerate(lc_rec.spectrum_set.order_by('id').all()):
            prefix = "spectrum%d_" % (i+1)
            data[prefix + 'id'] = spectrum.id
            data[prefix + 'id_display'] = spectrum.id
            data[prefix + 'mass_spectra_type'] = spectrum.mass_spectra_type_id,
            data[prefix + 'description'] = spectrum.description
            data[prefix + 'ionization_mode'] = lc_rec.method.ionization_mode.name
            data[prefix + 'polarity'] = lc_rec.method.polarity_name
            data[prefix + 'precursor_type'] = spectrum.precursor_type_id
            data[prefix + 'precursor_selection'] = spectrum.precursor_selection_id
            data[prefix + 'collison_energy'] = spectrum.collison_energy
            data[prefix + 'mass_spectra'] = format_mass_spectra(spectrum.point_set)

        return data

# Implementation 

def format_mass_spectra(point_set):
    return "\n".join(["%s    %s" % (str(p.x),str(p.y)) for p in point_set.all()])

def vetted_by(compound):
    if compound.is_gcma:
        filter = {'gc_record': models.GCMARecord.objects.get(pk=compound.pk)}
    if compound.is_lcma:
        filter = {'lc_record': models.LCMARecord.objects.get(pk=compound.pk)}
        
    vetted_by = "\n".join(["%s on %s" % (rv.user.get_profile().full_name, rv.record_vetted_on) 
        for rv in models.MARecordVet.objects.filter(**filter)])

    return vetted_by

def file_field_to_url(field):
    url = 'N/A'
    if field.name:
        url = '<a href="%s" target="_blank">%s</a>' % (field.url, field.name)
    return url

def validate_metabolite(req):
    errors = {}
    for param in req:
        if param.endswith('mass_spectra'):
            try:
                spectra = [decimal.Decimal(p) for p in req.get(param, '').split()]
                if len(spectra) % 2 != 0:
                    raise ArgumentError('Odd number of numbers received for spectra')
            except:
                errors[param] = "Should be even number of numbers delimited by whitespace."

    return errors   


