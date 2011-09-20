"""
Imports mass-spectral data of compounds from a NIST file into the DB.

To import all entries from a file invoke import_file(filename).
Django's ORM is used to save the entities to the DB, so the easiest
way to run the import is from a Django shell (ie. ./manage.py shell or
./manage.py shell_plus if you have Django extensions installed).
Every Compound and all its Points are saved in one transaction.
"""

from decimal import Decimal
import os
from mamboms.mambomsapp import models
from django.db import transaction

def import_file(filename, dataset_name='NIST'):
    assert is_valid_nist_file(filename), \
            "'%s' doesn't seem to be a valid NIST file!" % filename
    dataset_qs = models.Dataset.objects.filter(name=dataset_name)
    assert len(dataset_qs) == 1, \
        "Couldn't identify a unique dataset with name '%s'" % dataset_name 
    dataset = dataset_qs[0]
    with open(filename) as f:
        for i, nist_entry in enumerate(NistEntryReader(f)):
            (compound, points) = convert_nist_to_models(nist_entry, dataset)
            save_models(compound, points)

def is_valid_nist_file(filename):
    if not os.path.isfile(filename): return False
    with open(filename) as f:
        first_line = f.readline()
        if first_line.startswith('##TITLE'): return True
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

def convert_nist_to_models(nist_entry,dataset):
    return compound(nist_entry,dataset), points(nist_entry) 

def compound(nist_entry,dataset):
    return models.Compound(
                name = nist_entry['CAS NAME'],
                dataset = dataset,
                cas_regno = nist_entry['CAS REGISTRY NO'],
                molecular_formula = nist_entry['MOLFORM'],
                molecular_weight = Decimal(nist_entry['MW']) )

def points(nist_entry):
    return tuple(
        [ models.Point(x=int(p[0]), y=int(p[1])) 
                for p in nist_entry['XYDATA'] ]
    )

@transaction.commit_on_success
def save_models(compound, points):
    compound.save()
    for point in points:
        compound.point_set.add(point)
