
from django.contrib.auth.models import User, Group, Permission
from mamboms.mambomsapp import models

superusers = ('bpower@ccg.murdoch.edu.au', 'sdayalan@unimelb.edu.au')
nodereps = ('tszabo@ccg.murdoch.edu.au',)
noderep_editable_models = (models.Instrument, models.GCMethod, models.Column, models.BiologicalSystem, models.LCMethod, models.LCModification, models.MetaboliteClass, models.MassSpectraType) 

def set_superusers():
    for username in superusers:
        user = User.objects.get(username=username)
        user.is_superuser = True
        user.save()

def set_nodereps():
    noderep_group = Group.objects.get(name='NodeRep')
    for username in nodereps:
        user = User.objects.get(username=username)
        user.groups.add(noderep_group)

def set_noderep_permissions():
    noderep_group = Group.objects.get(name='NodeRep')
    for model in noderep_editable_models:
        for p in Permission.objects.all():
            if p.content_type.model_class() == model:
                noderep_group.permissions.add(p)

def main():
    set_superusers()
    set_nodereps()
    set_noderep_permissions()
