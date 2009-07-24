from django.db import models
from mamboms.webhelpers import *

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.name    

class Compound(models.Model):
    dataset = models.ForeignKey(Dataset)
    name = models.TextField()
    cas_regno = models.CharField(max_length=255)
    molecular_formula = models.CharField(max_length=255)
    molecular_weight = models.DecimalField(max_digits=10, decimal_places=3)

    def link_to_graph(self):
        return '<a href="%s%d">%s</a>' % (url('/mamboms/graph/'), self.id, 'Graph')
    link_to_graph.allow_tags = True
    link_to_graph.short_description = 'graph'

    def link_to_dotsearch(self):
        return '<a href="%s%d/%d/">%s</a>' % (url('/mamboms/search/dot/'), self.id, 50, 'Dot')
    link_to_dotsearch.allow_tags = True
    link_to_dotsearch.short_description = 'dotsearch'

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
        return [p.x for p in self.point_set.all()]

    @property
    def ys(self):
        return [p.y for p in self.point_set.all()]

class Point(models.Model):
    compound = models.ForeignKey(Compound)
    x = models.PositiveIntegerField() 
    y = models.PositiveIntegerField() 

