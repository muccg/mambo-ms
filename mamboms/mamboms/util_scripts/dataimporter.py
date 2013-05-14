"""
Imports mass-spectral data of compounds from a NIST file into the DB.

To import all entries from a file invoke import_file(filename).
Django's ORM is used to save the entities to the DB, so the easiest
way to run the import is from a Django shell (ie. ./manage.py shell or
./manage.py shell_plus if you have Django extensions installed).
"""
from decimal import Decimal
from mamboms.mambomsapp import models
from django.contrib.auth.models import User

from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from ccg.utils.webhelpers import siteurl
from mamboms.mambomsapp.views.utils import json_encode
import re

#for model introspection
from django.db.models.fields import DecimalField, BooleanField, TextField, CharField, IntegerField, FloatField
from mamboms.mambomsapp.models import GCMARecord, LCMARecord, Compound
from django.db.models.fields.related import ForeignKey, ManyToOneRel, ManyToManyField

import logging
logger = logging.getLogger('mamboms_import_log')


#for data parsing from files.
import datahandlers

#These constants are based on the strings in the database for the three datasets.
#javascript deliberately uses these strings, and if they ever change in the DB, 
#they need to change here and in the JS. 
DATASET_NIST = 'NIST'
DATASET_GCMA = 'MA GC'
DATASET_LCMA = 'MA LC'

MODEL_MAPPINGS = {}
MODEL_MAPPINGS[DATASET_NIST] = Compound
MODEL_MAPPINGS[DATASET_GCMA] = GCMARecord 
MODEL_MAPPINGS[DATASET_LCMA] = LCMARecord

#these are the three session variables we will set -
#the name of the uploaded file for an import,
#the dataset they will be operating on
#and the field mapping the user has configured
SESSION_IMPORT_FILENAME_KEY = 'import_filename'
SESSION_IMPORT_FIELDMAP_KEY = 'import_fieldmap'
SESSION_IMPORT_DATASET_KEY = 'import_dataset'


def main(limit=None):
    import_file('../docs/nist08_fixed.jca', limit)

def get_importable_fields(dataset):
    '''Return the set of importable fieldnames (displayname, fieldname) for 
       a dataset. '''
    importable_fields = []
    IModel = None #IModel is the model you will be introspecting
    if dataset == DATASET_GCMA:
        IModel = GCMARecord    
    elif dataset == DATASET_LCMA:
        IModel = LCMARecord
    elif dataset == DATASET_NIST:
        IModel = Compound
    else:
        raise Exception("Unsupported dataset type: %s" % (dataset))
    
    #introspect the model:
    for field in IModel._meta.fields:
        #The field 'known' is a special case. It is non importable, so ignore it if you find it.
        if field.name is 'known':
            pass
        elif type(field) in [DecimalField, BooleanField, TextField, CharField, IntegerField, FloatField]:
            canBeNull = field.null
            if type(field) in [TextField, CharField]: 
                canBeNull = True #if they pass no value, we will set the empty string
            importable_fields.append({"id" : field.name, "display" : field.verbose_name, "null": canBeNull})

    return importable_fields

def datafile_upload(request):
    #handle the uploaded file
    #store the filename in the session for later use
    #parse the file, get metadata about its fields, and an example of an entry.
    #also contains information about which dataset this is.
    #return the metadata, and how many records we think we have.
    retval = {}
    retval["success"] = True
    retval["text"] = ""

    fileobj = request.FILES.get('datafile', None)
    dataset = request.POST.get('dataset', None)
    try:
        filename = datahandlers.save_uploaded_file(fileobj)
        if filename:
            logger.debug("Saved upload as %s" % (filename))
        file_data_result = datahandlers.extract_file_data(filename)
        logger.debug("File data result was: %s" % (str(file_data_result)) )
        metadata = file_data_result["metadata"]
        errorstring = file_data_result["data"]["error"]
        if metadata is None or errorstring is not None:
            errorstring = "%s\n%s" % ("File %s could not be parsed for dataset %s" % (filename, dataset), errorstring)
            raise Exception(errorstring)
        
        metadata["dataset"] = dataset
        importable_fields = get_importable_fields(dataset)
        metadata["importable_fields"] = importable_fields
        retval["metadata"] = metadata
        retval["success"] = True 
        request.session[SESSION_IMPORT_FILENAME_KEY] = filename
        request.session[SESSION_IMPORT_DATASET_KEY] = dataset
    except Exception, e:
        logger.warning("Exception occured in upload step: %s" % ( e ) )
        retval["success"] = False
        retval["text"] = str(e)

    return HttpResponse(json_encode(retval))

def define_fields(request):
    #fields to associate in the file and in the database records, 
    #as well as default fields for record fields that arent in the file.
    #plus the data to use for fields which can never come from the file (uploader, for instance).
    #returns info on how many records would be created, how many would fail, etc.
    #would be good to return line numbers of broken lines.
    field_definitions = {} 
    for fieldname in request.POST.keys():
        #print "POST fieldname %s, value %s, type:%s" % (fieldname, request.POST.get(fieldname, None), str(type(request.POST.get(fieldname, None))) )
        #field_definitions[fieldname] = request.POST.get(fieldname, None)
        if len(request.POST.getlist(fieldname) ) > 1:
            field_definitions[fieldname] = request.POST.getlist(fieldname)
        else:
            field_definitions[fieldname] = request.POST.get(fieldname, None)

    filename = request.session[SESSION_IMPORT_FILENAME_KEY]
    dataset = request.session[SESSION_IMPORT_DATASET_KEY]
    #save the field defs
    request.session[SESSION_IMPORT_FIELDMAP_KEY] = field_definitions
    
    dry_run_import_result = import_data(filename, field_definitions, dataset, dryrun=True)
    if len(dry_run_import_result['failed'].keys()) == 0:
        dry_run_import_result["success"] = True
        dry_run_import_result["text"] = "Some records failed to import"
    else:
        dry_run_import_result["success"] = False
        dry_run_import_result["text"] = ""

    return HttpResponse(json_encode(dry_run_import_result))

def confirm_import(request):
    #confirms that the user wants to do the import with 
    #the filename in the session and
    #the data definition in the session.
    #essentially the same as the dry run, but actually saving the models.
    #returns report on the result of the action.
    filename = request.session[SESSION_IMPORT_FILENAME_KEY]
    dataset = request.session[SESSION_IMPORT_DATASET_KEY]
    field_definitions = request.session[SESSION_IMPORT_FIELDMAP_KEY]

    import_result = import_data(filename, field_definitions, dataset, dryrun=False)
    if len(import_result['failed'].keys()) == 0:
        import_result["success"] = True
        import_result["text"] = "Failed/partial import: Please restore a database backup."
    else:
        import_result["success"] = False
        import_result["text"] = ""
    #unset the session keys
    del request.session[SESSION_IMPORT_FIELDMAP_KEY]
    del request.session[SESSION_IMPORT_DATASET_KEY]
    del request.session[SESSION_IMPORT_FILENAME_KEY]
    return HttpResponse(json_encode(import_result))


# all fields are passed through as a list. Likely they will only contain one value
def import_data(filename, fieldmap, dataset=DATASET_NIST, dryrun=False):
    
    dataset_rec= models.Dataset.objects.get(name=dataset)    
    imported_records = 0
    error_records = 0
    file_data = datahandlers.extract_file_data(filename)
    data = file_data["data"]["data"]
    logger.debug('extracted file data is %s' % (str(data)) ) 
    metadata = file_data["metadata"]
    failed = {}
    passed = 0
    count = 0
    manytomany_dict = {}
    phase="Import"
    ismanytomany = False
    spectrumpoints = None #setting to None makes sure no spectrum is saved.
    for recordid in data.keys():
        try:
            #instantiate a model instance
            phase="Create Model"
            candidate = MODEL_MAPPINGS[dataset]()
            for fieldname in fieldmap.keys():
                ismanytomany = False
                logger.debug('fieldname is %s, data is %s, type is %s' % (fieldname, fieldmap[fieldname], str(type(fieldmap[fieldname])) ) )
                fielddata = fieldmap[fieldname]
                value = None
                matches = None
                if not isinstance(fielddata, list):
                    matches = re.match(r"\[\[(Field) (.*)\]\]", fielddata)
                #Are we assigning a 'static' value, or one from a parsed record field?
                if not matches:
                    phase="Literal data"
                    value = fielddata
                else:
                    phase="Substitute fields"
                    record_field = matches.group(2)
                    #the result will always come back as a STR, but it could be an int.
                    #lets try
                    try:
                        record_field = int(str(record_field))
                    except:
                        pass

                    value = data[recordid].get_value(record_field)
            
                if fieldname == 'spectrumfield':
                    spectrumpoints = value
                else:
                    #If this is a foreign key, we need to go get it
                    model_field = candidate._meta.get_field_by_name(fieldname)[0]
                    if isinstance(model_field, ForeignKey):
                        
                        phase="Foreign Key"
                        key = int(value)
                        rel_model = model_field.rel.to
                        value = rel_model.objects.get(id=key)
                        logger.debug("Foreign key %d for %s resolved to %s" % (key, fieldname, value ) )
                    #if this is a many to many field, we need to attach the data
                    #after the save
                    elif isinstance(model_field, ManyToManyField):
                        phase="Many to Many"
                        ismanytomany = True
                        #the data could either be a single value, or a list.
                        valueslist = []
                        
                        
                        if isinstance(value, list):
                            a = [int(n) for n in value]
                            valueslist = set(a) #make unique
                        else:
                            valueslist = [int(value)]
                        #now see if we can get all the related data.
                        resolved_list = []
                        for item in valueslist:
                            rel_model = model_field.rel.to
                            value = rel_model.objects.get(id=item)
                            resolved_list.append(value)
                        #now store the list of resolved records against the NAME of the many to many field manager
                        #manytomany_dict["%s_set" % (fieldname)] = resolved_list
                        manytomany_dict[fieldname] = resolved_list

                    #Only do the setattr if this isnt a many to many field.
                    if not ismanytomany:
                        logger.debug("%s: Not many to many" % (fieldname))
                        #First, if the value is empty, and null=True,
                        #then set the value to None, and pass to the db.
                        #If null=False and the field has 'blank=True', then
                        #leave the value alone - the model will know what to do with it
                        
                        if str(value) is "" and model_field.blank:
                            logger.debug("%s: empty value and field can be blank" % (fieldname))
                            if model_field.null:
                                value = None
                            else:
                                logger.debug('Value %s was blank, field blank=True, leaving alone' % (fieldname) )
                        else:
                            #cast the value in specific cases
                            if isinstance(model_field, DecimalField):
                                logger.debug("Cast decimal")
                                value = Decimal(value)
                            if isinstance(model_field, BooleanField):
                                logger.debug("Cast bool")
                                if value is None:
                                    value = False
                                elif value.lower() == 'false':
                                    value = False
                                elif value.lower() == 'true':
                                    value = True
                                else:
                                    value = False
                        
                        phase = "%s (field=%s, value=%s)" % (phase, fieldname, value)
                        logger.debug("Setting field: %s" % phase)
                        setattr(candidate, fieldname, value)
           
                candidate.dataset = dataset_rec 

            if dryrun:
                logger.debug("Doing full clean, candidate.method = %s" % (str(candidate.method)) )
                
                candidate.full_clean() #this causes django to validate the model, but not save
                #We cant test spectrum with 'full clean' because we cant link it 
                #to an unsaved compound. Instead, we just check that the
                #'createSpectrumFromPoints' function can successfully parse
                #the points (it will throw if it can't)
                if spectrumpoints is not None:
                    phase="Checking Spectrum"
                    spectrum = createSpectrumFromPoints(spectrumpoints)
                    
            else:
                logger.debug("Saving model")
                save_models(candidate, spectrumpoints)
                logger.debug("Attaching many to many fields")
                for key in manytomany_dict.keys():
                    logger.debug("mtom_key: %s, value %s" % (key, manytomany_dict[key]))
                candidate.save()
                #now we attach all the many to many fields.
                for mtomfield in manytomany_dict.keys():
                    for item in manytomany_dict[mtomfield]:
                        phase = "Adding mtom item (mtom=%s, item=%s" % (str(mtomfield), str(item))
                        mgr = getattr(candidate, mtomfield)
                        mgr.add(item)
                        #mtomfield.add(item)
                #candidate.save()
            
            
            passed += 1
        except Exception, e:
            logger.warning("Error: %s (%s)" % (e, phase))
            failed[count] = str("Error: %s (%s)" % (e, phase))
        count += 1        
    ret =  {"passed": passed, "failed": failed, "dataset": dataset} 
    return ret

def createSpectrumFromPoints(points):
    flat_points = []
    for p in points: 
        flat_points.extend( (str(p[0]), str(p[1])) )
    csv_points = ",".join(flat_points)
    spectrum = models.Spectrum()
    spectrum.raw_points = csv_points
    return spectrum 

@transaction.commit_on_success
def save_models(compound, points = None):
    compound.save()
    if points is not None:
        spectrum = createSpectrumFromPoints(points)
        compound.spectrum_set.add(spectrum)

