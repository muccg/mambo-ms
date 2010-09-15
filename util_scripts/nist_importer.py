"""
Imports mass-spectral data of compounds from a NIST file into the DB.

To import all entries from a file invoke import_file(filename).
Django's ORM is used to save the entities to the DB, so the easiest
way to run the import is from a Django shell (ie. ./manage.py shell or
./manage.py shell_plus if you have Django extensions installed).
"""

from decimal import Decimal
import os, sys
import os.path
from mamboms.mambomsapp import models
from django.contrib.auth.models import User

from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from mamboms.settings import WRITABLE_DIRECTORY
from webhelpers import siteurl
from mamboms.mambomsapp.views.utils import json_encode

def main(limit=None):
    import_file('../docs/nist08_fixed.jca', limit)

def handle_uploaded_file(f):
    print 'HANDLING DATA'
    name = os.path.join(WRITABLE_DIRECTORY, f.name)
    try:
        destination = open(name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        return name
    except Exception, e:
        print 'Error handling file upload, %s' % (str(e))
        
    return None

def data_import_view(request):
    if request.method=='GET':
        return data_import_present(request)
    else:
        return data_import_process(request)

def data_import_present(request):
    print 'IMPORT PRESENT'
    return render_to_response('mamboms/import_data.html', 
                                {'APP_SECURE_URL': siteurl(request),
                                 'username': request.user.username}
                             )   

def data_import_process(request):
    print 'IMPORT PROCESS'
    #use request.files[whatever], pass that object into the import file, with 
    #a param to indicate it is an already open file object.
    print str(request.POST)
    print str(request.FILES)
    filename = request.FILES.get('datafile', None)
    print 'filename is ', filename
    jsonresult = {}
    result = False
    try:
        fname = handle_uploaded_file(request.FILES.get('datafile'))
        dset = request.POST['dataset']
        print 'IMPORTING FILE'
        result = import_file(fname, limit=None, dataset_name=str(dset), extrafields = request.POST)
        if result:
            jsonresult['text'] = "Success. %d records imported." % (result)
        else:
            jsonresult['text'] = "An error occurred. No records imported."
    except Exception, e:
        result = False
        jsonresult['text'] = "Import failed: %s" % (str(e))

    jsonresult['success'] = bool(result)
    return HttpResponse(json_encode(jsonresult))

def import_file(filename, limit=None, dataset_name='NIST', extrafields=None):
    print 'IMPORT FILE'
    if not is_valid_nist_file(filename):
        print 'raising exception'
        raise Exception( "'%s' doesn't seem to be a valid NIST file!" % filename )
    print 'WAS VALID'
    dataset_qs = models.Dataset.objects.filter(name=dataset_name)
    if len(dataset_qs) != 1 : 
        raise Exception("Couldn't identify a unique dataset with name '%s'" % dataset_name )
    
    if limit is None:
        limit = sys.maxint
    dataset = dataset_qs[0]
    importedrecords = 0
    print 'BEFOR WITH'
    with open(filename) as f:
        print 'INSIDE WITH'
        for i, nist_entry in enumerate(NistEntryReader(f)):
            if i == limit: break
            (compound, points) = convert_nist_to_models(nist_entry, dataset, extrafields=extrafields)
            save_models(compound, points)
            importedrecords += 1
    return importedrecords

def is_valid_nist_file(filename):
    print 'filename is ', filename
    if not os.path.isfile(filename): return False
    print 'opening file' 
    with open(filename) as f:
        print 'reading file'
        first_line = f.readline()
        if first_line.startswith('##TITLE'): return True    
    print 'returning false'
    return False

class FileLineReader():
    def __init__(self, opened_file, ignore_empty=True):
        self.file = opened_file
        self.ignore_empty = ignore_empty
        self.reprocess_last_line = False
        self.last_line = None

    def readline(self):
        line = self.last_line if self.reprocess_last_line else self._next_line()
        self.reprocess_last_line = False
        return line

    def _next_line(self):
        eof = lambda line: line == ''
        ignore_line = lambda line: False
        if self.ignore_empty:
            ignore_line = lambda line: line.strip() == ''

        line = self.file.readline()
        while not eof(line) and ignore_line(line):
            line = self.file.readline()
        self.last_line = line
        return line

class NistEntryReader():
    def __init__(self, opened_file):
        self.reader = FileLineReader(opened_file)

    def next_line(self):
        return self.reader.readline()

    def read_points(self):
        points = []
        line = self.next_line()
        while line and not line.startswith('##'):
            (x,y) = line.strip().split()
            points.append((x.strip(),y.strip()))
            line = self.next_line()
        if line.startswith('##'): 
            self.reader.reprocess_last_line = True
        return points

    def key_from_line(self, line):
        return line[2:line.index('=')].strip()

    def value_from_line(self, line, key):
        if key == 'XYDATA':
            return self.read_points()
        else:
            return line[line.index('=')+1:].strip()

    def __iter__(self):
        entry = {}
        line = self.next_line()
        while line:
            key = self.key_from_line(line)
            value = self.value_from_line(line,key)
            if key not in entry:
                entry[key] = value
            else:
                yield entry
                entry = {key:value}
            line = self.next_line()
        yield entry

def convert_nist_to_models(nist_entry,dataset, extrafields=None):
    return compound(nist_entry,dataset, extrafields=extrafields), points(nist_entry) 

def compound(nist_entry,dataset, extrafields=None):
    if dataset.name.strip() == 'MA GC':
        column = models.Column.objects.get(id=extrafields['column'])
        known = extrafields.get('known', False) #not technically correct...
        instrument = models.Instrument.objects.get(id=extrafields['instrument'])
        runby = User.objects.get(username=extrafields['sample_run_by'])
        uploadedby = User.objects.get(username=extrafields['uploaded_by'])
        retentiontime = extrafields.get('retention_time', 0)
        node = models.Node.objects.get(name=extrafields['uploading_node'])
        description = extrafields['extract_description']
        method = models.GCMethod.objects.get(id=extrafields['method'])
        metaboliteclass = models.MetaboliteClass.objects.get(id=extrafields['metaboliteclass'])

        return models.GCMARecord(
                #compound fields
                cas_name = nist_entry['CAS NAME'],
                dataset = dataset,
                cas_regno = nist_entry['CAS REGISTRY NO'],
                molecular_formula = nist_entry['MOLFORM'],
                molecular_weight = Decimal(nist_entry['MW']), 
                #MA Record Base fields
                known = known,
                node = node,
                column = column,
                instrument = instrument,
                sample_run_by = runby,
                record_uploaded_by = uploadedby,
                retention_time = retentiontime,
                extract_description = description,
                metabolite_class = metaboliteclass,
                #GC fields
                method = method)
    elif dataset.name == 'MA LC':
        raise Exception('LC not supported')
    elif dataset.name == 'NIST':    
    
        return models.Compound(
                cas_name = nist_entry['CAS NAME'],
                dataset = dataset,
                cas_regno = nist_entry['CAS REGISTRY NO'],
                molecular_formula = nist_entry['MOLFORM'],
                molecular_weight = Decimal(nist_entry['MW']) )
    else:
        raise Exception('%s is not a known dataset' % (dataset))

    print 'end of function'

def points(nist_entry):
    return tuple(
        [ (int(p[0]),int(p[1])) for p in nist_entry['XYDATA'] ]
    )

@transaction.commit_on_success
def save_models(compound, points):
    flat_points = []
    for p in points: 
        flat_points.extend( (str(p[0]), str(p[1])) )
    csv_points = ",".join(flat_points)
    spectrum = models.Spectrum()
    spectrum.raw_points = csv_points
    compound.save()
    compound.spectrum_set.add(spectrum)
