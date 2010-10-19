from django.db import models
from models import *

class Compounds_View(models.Model):
    dataset = models.ForeignKey(Dataset)
    compound_name = models.CharField(null=True, max_length=255)
    cas_name = models.CharField(null=True,max_length=255)
    cas_regno = models.CharField(max_length=255)
    molecular_formula = models.CharField(max_length=255)
    molecular_weight = models.DecimalField(max_digits=10, decimal_places=3)
    instrument = models.ForeignKey(Instrument)
    metabolite_class = models.ForeignKey(MetaboliteClass)
    retention_time = models.CharField(max_length=255) 
    derivitization_agent = models.CharField(max_length=255)
    biological_system = models.ForeignKey(BiologicalSystem)
    mono_isotopic_mass = models.CharField(max_length=255)
    chromatography_type = models.ForeignKey(ChromatographyType)
    ionization_mode = models.ForeignKey(IonizationMode)
    ms_geometry = models.ForeignKey(MSGeometry)
    polarity = models.CharField(max_length=1, choices=MethodBase.POLARITY_CHOICES)
    
    def save(*args, **kwargs):
        '''prevent people accidentally saving - this is a view, not an actual table'''
        assert False, 'Do not call save on this model, it is a view.' 
