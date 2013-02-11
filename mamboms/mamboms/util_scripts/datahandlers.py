"""
The functions in this file are called by the functions in
dataimport.py, which are exposed via the web.

These functions do all the heavy lifting of parsing various file formats
into an MSDataRecord, so they can be processed by the dataimport functions.
"""

import os, sys
import os.path
from django.conf import settings 
import csv
import logging
logger = logging.getLogger('mamboms_import_log')

class MSDataRecord(object):
    def __init__(self):
        self._data = {}
    def set_value(self, fieldname, value):
        self._data[fieldname] = value;

    def get_value(self, fieldname):
        return self._data[fieldname]
    
    def import_list(self, datalist):
        '''this is for importing values where there are no
           matching fieldnames '''
        for d in range(len(datalist)):
            self.set_value(d, datalist[d])

    def import_dict(self, datadict):
        '''this is for importing a fieldname:value dict'''
        for field in datadict.keys():
            self.set_value(field, datadict[field])
   
    def import_data(self, data):
        if isinstance(data, dict):
            self.import_dict(data)
        if isinstance(data, list):
            self.import_list(data)

    def get_data(self):
        return self._data

    def num_fields(self):
        return len(self._data.keys())


def save_uploaded_file(f):
    name = os.path.join(settings.CCG_WRITEABLE_DIRECTORY, f.name)
    try:
        destination = open(name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        return name
    except Exception, e:
        logger.warning('Error handling file upload, %s' % (str(e)) )
        
    return None 


def extract_file_data(filename):
    parseddata = None
    success = False
    try:
        with open(filename) as f:
            if is_valid_nist_file(filename):
                reader = NistEntryReader(f)
            else:
                reader = CSVEntryReader(f)

            parseddata = parseData(reader)
            success = True
    except Exception, e:
        logger.debug("Exception parsing data: %s" % (e))

    metadata = None
    
    if parseddata is not None:
        metadata = {}
        metadata["dataset"] = None
        metadata["num_records"] = parseddata["numrecords"]
        metadata["min_fields"] = parseddata["data"][parseddata["minindex"]].num_fields()
        metadata["max_fields"] = parseddata["data"][parseddata["maxindex"]].num_fields()
        metadata["sampledata"] = parseddata["data"][parseddata["maxindex"]].get_data()

    return {"data": parseddata, "metadata": metadata}


def is_valid_nist_file(filename):
    if not os.path.isfile(filename): return False
    with open(filename) as f:
        first_line = f.readline()
        if first_line.startswith('##TITLE'): 
            logger.debug("%s was a valid JCA* file" % (filename))
            return True    
    logger.debug('%s was not a JCA* file' % (filename) )
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

class CSVEntryReader():
    def __init__(self, opened_file):
        self.reader = csv.reader(opened_file, delimiter=',')

    def __iter__(self):
        rowdata = self.reader.next()
        while rowdata:
            while rowdata[0].strip().startswith('#'):
                rowdata = self.reader.next()
            yield rowdata
            rowdata = self.reader.next()
        yield rowdata


def parseData(reader):
    count = 0
    data = {}
    minrecord = None
    maxrecord = None
    minrecordindex = 0
    maxrecordindex = 0
    numrecords = 0
    error = None
    try:
        for entry in reader:
            data[count] = MSDataRecord()
            data[count].import_data(entry)
            if minrecord is None or len(minrecord) > len(entry):
                minrecord = entry 
                minrecordindex = count
            if maxrecord is None or len(maxrecord) < len(entry):
                maxrecord = entry 
                maxrecordindex = count
            numrecords += 1    
            count += 1
    except Exception, e:
        error = "%s [The first %d records were successfully parsed] [last line processed was: %s]" % (str(e), numrecords, reader.reader.last_line)

    ret = {"data": data, "minindex": minrecordindex, "maxindex": maxrecordindex, "numrecords": numrecords, "error": error }    
    return ret
