import datetime
from decimal import Decimal
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.webhelpers import *

class NotAuthorizedError(StandardError):
    pass


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.name    

class Compound(models.Model):
    dataset = models.ForeignKey(Dataset)
    # null for NIST
    compound_name = models.CharField(blank=True,max_length=255, verbose_name="Compound Name")
    cas_name = models.TextField(blank=True, verbose_name="CAS Name")
    cas_regno = models.CharField(max_length=255, blank=True, verbose_name="CAS Registration Number")
    molecular_formula = models.CharField(max_length=255, blank=True, verbose_name="Molecular Formula")
    molecular_weight = models.DecimalField(max_digits=18, decimal_places=10, verbose_name="Molecular Weight", default=Decimal("0.0"))

    def link_to_graph(self):
        return '<a href="%s%d/">%s</a>' % (url('/mamboms/graph/'), self.id, 'Graph')
    link_to_graph.allow_tags = True
    link_to_graph.short_description = 'graph'

    def truncated_name(self):
        w = 100
        if len(self.name) > w:
            ln = len(self.name)
            n = self.name[0:w//2] + ' ... ' + self.name[ln-w//2:]
        else:
            n = self.name

        return n
    
    truncated_name.short_description = 'name'

    @property
    def xs(self):
        return [float(str(p.x)) for p in self.point_set.all()]

    @property
    def ys(self):
        return [float(str(p.y)) for p in self.point_set.all()]

    @property
    def spectrum(self):
        return self.spectrum_set.all()[0] if self.spectrum_set.all() else None

    @property
    def point_set(self):
        return self.spectrum.point_set if self.spectrum else PointSet('')

    @property
    def is_gcma(self):
        try:
            self.gcmarecord
        except GCMARecord.DoesNotExist:
            return False
        else:
            return True

    @property
    def is_lcma(self):
        try:
            self.lcmarecord
        except LCMARecord.DoesNotExist:
            return False
        else:
            return True

    @property
    def record_uploaded_by(self):
        if self.is_gcma:
            return self.gcmarecord.record_uploaded_by 
        elif self.is_lcma: 
            return self.lcmarecord.record_uploaded_by 
        return None

    @property
    def node(self):
        if self.is_gcma:
            return self.gcmarecord.node 
        elif self.is_lcma: 
            return self.lcmarecord.node 
        return None

    def can_be_deleted_by(self, user):
        if not (self.is_gcma or self.is_lcma):
            return False
        profile = user.get_profile()
        return (profile.is_admin or (profile.is_noderep and profile.node == self.node.name))
       
    def delete_by(self, user):
        if not self.can_be_deleted_by(user):
            raise NotAuthorizedError()
        super(Compound, self).delete()
 
    @property
    def record_vets(self):    
        assert (self.is_gcma or self.is_lcma), "Only GCMA and LCMA record have vets"
        if self.is_gcma:
            return self.gcmarecord.record_vets
        elif self.is_lcma: 
            return self.lcmarecord.record_vets

    def can_be_vetted_by(self, user):
        profile = user.get_profile()
        return (
            self.record_uploaded_by != user 
            and user not in self.record_vets.all()
            and profile.is_noderep and profile.node != self.node)

    def vet(self, user):
        if not self.can_be_vetted_by(user):
            raise NotAuthorizedError()
        vet = MARecordVet()
        vet.user = user
        vet.set_compound(self)
        vet.record_vetted_on = datetime.date.today()
        vet.save()

class PointSet:
    def __init__(self, raw_points):
        self._raw_points = raw_points

    def all(self):
        l = self._raw_points.split(',')
        return [Point(Decimal(x),Decimal(y)) for x, y in zip(l[::2], l[1::2])]

    def first(self, predicate=None):
        if predicate is None:
            predicate = lambda p: True
        for p in self.all():
            if predicate(p): 
                return p

    def round(self, f):
        if( (f-int(f) < 0.7) and (f - int(f)) >= -0.3):
            return int(f)
        else:
            return int(f)+1


    def get_rounded(self):
        l = (self._raw_points).split(',')
        return[Point(self.round(Decimal(x)), Decimal(y)) for x,y in zip(l[::2], l[1::2])]


class Point():
    '''This used to be a Django model, but now we store the points as a raw
    comma-separated points. 
    This class and PointSet are used to keep the same API working.'''

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

class Node(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class ChromatographyType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class MSGeometry(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'MS Geometry'

    def __unicode__(self):
        return self.name

class IonizationMode(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Instrument(models.Model):
    node = models.ForeignKey(Node)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(settings.PERSISTENT_FILESTORE, settings.PERSISTENT_FILESTORE_URL)

class MethodBase(models.Model):
    '''Common fields of GC Methods and LC Methods'''
    POLARITY_CHOICES = (
        ('P', 'Positive'),
        ('N', 'Negative'),
    )    

    FILE_PREFIX = 'methods'

    class Meta:
        abstract = True

    node = models.ForeignKey(Node)
    name = models.CharField(max_length=255)
    chromatography_type = models.ForeignKey(ChromatographyType)
    ms_geometry = models.ForeignKey(MSGeometry, verbose_name='MS Geometry')
    ionization_mode = models.ForeignKey(IonizationMode)
    polarity = models.CharField(max_length=1, choices=POLARITY_CHOICES)
    derivitization_agent = models.CharField(max_length=255) 
    mass_range_acquired = models.CharField(max_length=255, verbose_name='Mass Range Acquired') 
    instrument_method = models.FileField("Instrument Method (Proprietary file)",
            upload_to='method/instrument', storage=fs, max_length=500, null=True)
    method_summary = models.FileField("Method Summary (Text file)",
            upload_to='method/summary', storage=fs, max_length=500, null=True)

    @property
    def polarity_name(self):
        return dict(MethodBase.POLARITY_CHOICES)[self.polarity] 

    @property
    def platform(self):
        return "%s - %s - %s" % (
            self.chromatography_type.name, self.ms_geometry.name, self.polarity)

    def __unicode__(self):
        return self.name

class GCMethod(MethodBase):
    class Meta:
        verbose_name = 'GC Method'

    mass_exp_deriv_adducts = models.CharField(max_length=255, verbose_name='Mass of Expected Derivitization Adducts') 

    @property
    def platform(self):
        polarity = dict(GCMethod.POLARITY_CHOICES)[self.polarity]
        return "%s - %s - %s" % (
            self.chromatography_type.name, self.ms_geometry.name, polarity)

class LCMethod(MethodBase):
    class Meta:
        verbose_name = 'LC Method'

    mz_exp_deriv_adducts = models.CharField(max_length=255, verbose_name='m/z of Expected Derivitization Adducts') 
    flow_rate = models.CharField(max_length=255) 
    solvent_composition_a = models.CharField(max_length=255) 
    solvent_composition_b = models.CharField(max_length=255) 
    solvent_composition_c = models.CharField(max_length=255) 
    solvent_composition_d = models.CharField(max_length=255) 

class LCModification(models.Model):
    class Meta:
        verbose_name = 'LC Modification'

    name_of_compound = models.CharField(max_length=255)
    mass = models.CharField(max_length=255)
    molecular_formula = models.CharField(max_length=255)

    #Google Code issue #41, mass field should be 
    #called 'Accurate Mass' in admin.
    mass.verbose_name = 'Accurate Mass' 

    def __unicode__(self):
        return self.name_of_compound

class Column(models.Model):
    node = models.ForeignKey(Node)
    chromatography_type = models.ForeignKey(ChromatographyType)
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    length = models.CharField(max_length=255)
    internal_diameter = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    dimension = models.CharField(max_length=255)
    guard_column = models.CharField(max_length=255)
    product_number = models.CharField(max_length=255)
    particle_size = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class BiologicalSystem(models.Model):
    kingdom = models.CharField(max_length=255)
    species = models.CharField(max_length=255)

    def __unicode__(self):
        return self.kingdom + " - " + self.species

class MARecordVet(models.Model):
    #ma_record = models.ForeignKey('MARecordBase')
    # You can't have a foreign key that points to an abstract class in Django
    # so instead of the line above we use the 2 lines below
    gc_record = models.ForeignKey('GCMARecord', null=True)
    lc_record = models.ForeignKey('LCMARecord', null=True)

    user = models.ForeignKey(User)
    record_vetted_on = models.DateField(auto_now_add=True)
    
    def set_compound(self, compound):
        assert (compound.is_gcma or compound.is_lcma), "Only GCMA or LCMA records can be vetted"
        if compound.is_gcma:
            self.gc_record = GCMARecord.objects.get(pk=compound.pk)
        if compound.is_lcma:
            self.lc_record = LCMARecord.objects.get(pk=compound.pk)

class MetaboliteClass(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Metabolite Classes'

    def __unicode__(self):
        return self.name

class MARecordBase(Compound):
    class Meta:
        abstract = True

    FILE_PREFIX = 'marecord'

    known = models.BooleanField(verbose_name="Known")
    node = models.ForeignKey(Node, verbose_name="Uploading Node")
    instrument = models.ForeignKey(Instrument, verbose_name="Instrument")
    column = models.ForeignKey(Column, verbose_name="Column")
    sample_run_by = models.ForeignKey(User, related_name='%(class)s_ran', verbose_name="Sample Run By")
    record_uploaded_by = models.ForeignKey(User, related_name='%(class)s_uploaded_records', verbose_name="Record Uploaded By")
    record_uploaded_on = models.DateField(auto_now_add=True, verbose_name="Record Uploaded Date")
    record_vets = models.ManyToManyField(User, through='MARecordVet', related_name='%(class)s_vetted_records')
    biological_systems = models.ManyToManyField(BiologicalSystem, verbose_name="Biological Systems")
    metabolite_class = models.ForeignKey(MetaboliteClass, verbose_name="Metabolite Class")
    retention_time = models.CharField(max_length=255, blank=True, verbose_name="Retention Time")   
    retention_index = models.CharField(max_length=255, blank=True, verbose_name="Retention Index")
    kegg_id = models.CharField(max_length=255, blank=True, verbose_name="KEGG ID")   
    kegg_link = models.CharField(max_length=255, blank=True, verbose_name="KEGG Link")   
    extract_description = models.TextField(verbose_name="Extract Description", blank=True)
    structure = models.FileField(upload_to='marecord/structure/', storage=fs, max_length=500, blank=True)
 
class GCMARecord(MARecordBase):
    method = models.ForeignKey(GCMethod)
    quant_ion = models.DecimalField(max_digits=10, decimal_places=3,null=True, blank=True, verbose_name="Quant Ion")
    qualifying_ion_1 = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, verbose_name="Qualifying Ion 1")
    qualifying_ion_2 = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, verbose_name="Qualifying Ion 2")
    qualifying_ion_3 = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, verbose_name="Qualifying Ion 3")
 
    class Meta:
        verbose_name = 'GC MA Record'
        
    def qualifying_ion_ratio(self, ion1, ion2):
        p1 = self.point_set.first(lambda p: p.x == ion1)
        p2 = self.point_set.first(lambda p: p.x == ion2)
        if p1 is not None and p2 is not None and p2.y:
            return p1.y / p2.y

    @property
    def qualifying_ion_ratio12(self):
        return self.qualifying_ion_ratio(self.qualifying_ion_1, self.qualifying_ion_2)

    @property
    def qualifying_ion_ratio23(self):
        return self.qualifying_ion_ratio(self.qualifying_ion_2, self.qualifying_ion_3)

class LCMARecord(MARecordBase):
    method = models.ForeignKey(LCMethod)
    mono_isotopic_mass = models.CharField(max_length=255, blank=True, verbose_name="Mono Isotopic Mass")
    class Meta:
        verbose_name = 'LC MA Record'

class Synonym(models.Model):
    ma_record = models.ForeignKey(Compound, related_name='synonyms')
    name = models.CharField(max_length=255)

class PrecursorType(models.Model):
    name = models.CharField(max_length=50)
    polarity = models.CharField(max_length=1, choices=MethodBase.POLARITY_CHOICES)
    def __unicode__(self):
        return self.name
        
class PrecursorSelection(models.Model):
    name = models.CharField(max_length=50)

class MassSpectraType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Spectrum(models.Model):
    '''NIST and GC records will have only one of these, but LC can have more than one'''
    compound = models.ForeignKey(Compound)
    raw_points = models.TextField()
    # Fields below applicable only to LC records, null for NIST and GC
    mass_spectra_type = models.ForeignKey(MassSpectraType, null=True, blank=True)
    description = models.TextField(blank=True)
    precursor_type = models.ForeignKey(PrecursorType, null=True, blank=True)
    precursor_selection = models.ForeignKey(PrecursorSelection, null=True, blank=True)
    collison_energy = models.CharField(max_length=255,blank=True)
    ionized_species = models.ManyToManyField(LCModification, null=True, blank=True)
    #As per Google Code issue #55
    precursor_mass = models.DecimalField(max_digits=18, decimal_places=10, verbose_name="Precursor Mass", default=Decimal("0.0"))
    precursor_ion = models.CharField(max_length=20, blank=True, null=True, verbose_name="Precursor Ion")
    product_ion = models.CharField(max_length=20, blank=True, null=True, verbose_name="Product Ion")
    fragment_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Fragment Type")
    
    @property
    def point_set(self):
        return PointSet(self.raw_points)

    @property
    def xs(self):
        return [float(str(p.x)) for p in self.point_set.all()]

    @property
    def ys(self):
        return [float(str(p.y)) for p in self.point_set.all()]


#class SpectrumIonizedSpecies(models.Model):
#    spectrum = models.ForeignKey(Spectrum)
#    ionized_species = models.ForeignKey(LCModification)


#a class to keep a list of updates for the hash
class HashMaintenance(models.Model):
    spectrum = models.ForeignKey(Spectrum)
    last_updated = models.DateField(auto_now=True)


#set up the post save hook for the spectrum...
from django.db.models.signals import post_save
def spectrum_post_save(sender, instance, created, **kwargs):
    #whether it was created or updated, we don't care.
    #either way, the hash is going to want to know about it.
    if created: #if created, we KNOW the spectrum cant be in our update list
        h = HashMaintenance()
    else:
        #otherwise, it could be: lets check
        try:
            h = HashMaintenance.objects.get(spectrum__id = instance__id)
            print 'Found updated spectrum in our update list'    
        except Exception, e:
            print 'Updated spectrum was not in our update list'    
            h = HashMaintenance() 
    
    #In all cases, update the 'spectrum' of h, and save
    h.spectrum = instance;
    h.save()

post_save.connect(spectrum_post_save, sender=Spectrum)
