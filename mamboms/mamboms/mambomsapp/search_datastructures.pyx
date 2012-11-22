import time
import gc
from pytc import *
import cPickle
#import cjson
import os
from django.conf import settings

#limits on how many records to import
chunk_size = 2000
#records = 10000

DATAHASH = [None]

#This implements the standard dot product formula, with an ma inhouse scaling factor:
#     Tcm**2            (sum(Iq * Il))**2
#  ------------  *   ---------------------
#  Tmq * Tml         (sum(Iq**2))(sum(Il**2))
#
# Where:
#   Tcm = Total number of common masses between query and library
#   Tmq = Total masses in query spectra
#   Tml = Total masses in library spectra
#   Iq = Intensity of common masses in query spectra
#   Il = Intensity of common masses in library spectra
#
def compute_comparison_ma_inhouse(l_dict, q_dict, common_masses):
    '''l_dict and q_dict are the library and query dicts respectively. 
    '''
    cdef float sum_IqIl = 0
    cdef float sum_Iq2 = 0
    cdef float sum_Il2 = 0
    cdef float l_y
    cdef float q_y
    cdef int tot_cm
    cdef int tot_mq
    cdef float A, B, C
    for mass in common_masses:
        l_y = float(l_dict[mass])
        q_y = float(q_dict[mass])
        sum_IqIl += l_y * q_y
        sum_Iq2 += q_y ** 2
        sum_Il2 += l_y ** 2

    tot_cm = len(common_masses)
    tot_mq = len(q_dict)
    A = float(tot_cm * tot_cm) / float(tot_mq * tot_mq)
    B = float(sum_IqIl * sum_IqIl) / float(sum_Iq2 * sum_Il2)
    C = A * B

    return C 

#This implements the standard dot product formula, with no scaling factor:
#    (sum(Iq * Il))**2
#   ---------------------
#   (sum(Iq**2))(sum(Il**2))
#
# Where:
#   Iq = Intensity of common masses in query spectra
#   Il = Intensity of common masses in library spectra
#

def compute_comparison_dotproduct(l_dict, q_dict, common_masses):
    '''l_dict and q_dict are the library and query dicts respectively. 
    '''
    cdef float sum_IqIl = 0
    cdef float sum_Iq2 = 0
    cdef float sum_Il2 = 0
    cdef float l_y
    cdef float q_y
    for mass in common_masses:
        l_y = float(l_dict[mass])
        q_y = float(q_dict[mass])
        sum_IqIl += l_y * q_y
        sum_Iq2 += q_y ** 2
        sum_Il2 += l_y ** 2

    return float(sum_IqIl * sum_IqIl) / float(sum_Iq2 * sum_Il2)

def y_ref_compare(int x, int y, int ref):
    if abs(ref-x) > abs(ref-y):
        return 1
    elif x==y:
        return 0
    else:
        return -1
def y_compare_tuple(x,y):
    cdef int a = x[1]
    cdef int b = y[1]
    if a > b:
        return 1
    elif a == b:
        return 0 
    else:
        return -1

def y_compare(x, y):
    cdef int a = x.y
    cdef int b = y.y
    if a > b:
        return 1
    elif a == b:
        return 0
    else:
        return -1

class MassIndex(object):
    '''base class for a datastructure which orders based mass'''
    def __init__(self, recordset, *args, **kwargs):
        pass

    def accumulate(self, recordset):
        '''Push more data into this datastructure'''
        pass

    def __getitem__(self, key):
        '''so that we can use [] notation'''
        pass

    def __setitem__(self, key, value):
        '''so that we can use [] notation'''
        pass


class TokyoHash(MassIndex):
   
    int_dict = HDB() # no options
    STATE_BUILDING = 0 #in the process of adding records
    STATE_CLEAN = 1    #ready for requests, structure up to date
    STATE_DIRTY = 2    #ready for requests, structure known to not have latest data
    STATE_EMPTY = 3

    def __init__(self, keyspace='nokeyspace'):
        #self.local_dict = {}
        #self.int_dict.KEYSPACE  = keyspace 
        self.state = self.STATE_EMPTY
        self.stats = {}
        self.stats['chunk_build_times'] = []
        self.build_start_time = None
        self.specs = 0
        w = HDBOWRITER
        c = HDBOCREAT
        
        hashfile = os.path.join(settings.WRITABLE_DIRECTORY, 'mahash_%s_.tch' % (keyspace))
        if not os.path.exists(hashfile):
            print 'Disk hash (%s) did not exist, creating new' % (str(hashfile))
            self.int_dict.open(hashfile, HDBOWRITER | HDBOCREAT )
            self['__total_records'] = 0
        else:
            print 'Disk hash already existed: %s' % (str(hashfile))
            self.int_dict.open(hashfile, HDBOWRITER )
            
        self.chunk_size = chunk_size
        self.records = 0

        print 'TokyoHash init finished'
        #self._build(recordset)
        return

    def status(self, numdirty=0):
        self['__total_dirty'] = numdirty
        if self.records > 0:
            perc = 100.0 * self.specs / float(self.records) 
        else:
            perc = 0
        self.stats['percentage'] = perc
        st = 'unknown'
        
        
        #some state logic
        if self.state != self.STATE_BUILDING:
            #if we have no keys or records, we are empty
            if self['__total_records'] == 0:
                self.state = self.STATE_EMPTY
            elif numdirty > 0:
                self.state = self.STATE_DIRTY
            else:
                self.state = self.STATE_CLEAN
        
        if self.state == self.STATE_EMPTY:
            st = 'empty'
        elif self.state == self.STATE_CLEAN:
            st = 'clean'
        elif self.state == self.STATE_DIRTY:
            st = 'dirty'
        elif self.state == self.STATE_BUILDING:
            st = 'building'
        
        self.stats['state'] = st
        self.stats['chunk_size'] = self.chunk_size
        self.stats['max_records_size'] = self.records
        self.stats['actual_record_count'] = self['__total_records']
        self.stats['pending_dirty_records'] = self['__total_dirty']
        self.stats['keys'] = len(self.int_dict.keys())

        return self.stats

    def clear_hash(self):
        print 'deleting all values in the hash'
        for k in self.int_dict.keys():
            del self.int_dict[k]
        self['__total_records'] = 0
        self.state = self.STATE_EMPTY
        

    def add_record(self, localdict, spec):
        l = localdict
        #the point_set property in models returns a PointSet, and then 
        #we use the 'get_rounded' function.
        #This allows us to not have to import anything
        #from models here, and hence this shared object
        #once built, can be kept away and decoupled from
        #the mamboms code

        points = spec.point_set.get_rounded()
        for point in points:
            x = int(point.x)
            y = int(point.y)
            if not l.has_key(x):
                l[x] = {} 

            #impossible for a compound to have two colliding masses (unless round function is screwing up 
            if not l[x].has_key(y):
                l[x][y] = []

            #TODO: We add the spec id to the values list if it isnt already there, 
            #BUT if this is an update, the id's for the old keys will still exist.
            #Essentially we need to do a search and remove the id from any [x][y] which
            #it occurs in, and then add the new values in. Or an optimised version of
            #such...
            if (int(spec.id) not in l[x][y]):
                l[x][y].append(int(spec.id)) #cast to int rather than use reference to db object
    

    
    def _accumulate(self, recordset, localdict):
        l = localdict 
        self.state = self.STATE_BUILDING
        for spec in recordset:
            self.specs += 1
            self['__total_records'] += 1;
            self.add_record(l, spec) 
    
    def _push(self, localdict):
        l = localdict
        #now push it all to memcache
        import sys
        try:
            for k in l.keys():
                v = l[k]
                if sys.getsizeof(v) > 1000000:
                    print 'value for %s was too big' % (str(k)) 
                
                #We are about to add the record. For accounting purposes, collect some stats.
                #if self[k] is None:
                #    prev = 0
                #else:
                #    prev = sum([ len c for c in self[k] ]) #sum of all id's in each y value
                #  
                self[k] = l[k]
                #
                #post = sum([len c for c in l[k] ])
                #delta = post - prev
                #self['__total_records'] += delta;


        except Exception, e:
            print 'Could not do a set: ', e

    def build(self, recordset, limit = None):
        if self.state == self.STATE_BUILDING:
            return

        self.state = self.STATE_BUILDING
        self.build_start_time = time.time()
        low = 0
        finished = False
        l = self.int_dict

        #Try to decode the int. If it is none, or you cant, then the limit is the entire set.
        try:
            self.records = int(limit)
        except Exception, e:
            self.records = recordset.count()
        
        print 'Building TokyoHash with limit: %d' % (self.records)
        while low <= self.records:
            cc = recordset 
            a = time.time()
            c = cc[low:low+chunk_size]
            ld = {}
            self._accumulate(c, ld)
            self.state = self.STATE_BUILDING #accumulate finishes with 'clean' state

            #del(c) #try to free up the record
            gc.collect()
       
            low += chunk_size
            tt = time.time() - a
            print low
            #self.stats['chunk_build_times'].append(tt)
            self.stats['most_recent_chunk_build_time'] = tt
            self.stats['most_recent_chunk_limits'] = "%s : %s" % (str(low), str(low+chunk_size))

        #now push.
        self._push(ld)

        #write to stats
        self.stats['build'] = time.time()-self.build_start_time
        self.state = self.STATE_CLEAN

        #we are at the end of the build process.
        #kill the localdict.
        ld = {}
        gc.collect()

    def __getitem__(self, key):
        #v = self.int_dict[key]
        #return [(k, v[k]) for k in v.keys()]
        try:
            return cPickle.loads(self.int_dict.get(str(key)))
        except Exception, e:
            #print '__getitem__ fail: ', e
            return None

    def __setitem__(self, key, value):
        '''this should be read only once we build it'''
        self.int_dict.put(str(key), cPickle.dumps(value))

    def find_matches(self, pointslist):
        ''' input is list of x,y tuples'''
        '''step one. sort the input x's based on intensity(y).'''
        sorted_points = sorted(pointslist, cmp=y_compare_tuple, reverse=True) #this could be slow - two function calls (properties) each sort...
        searchdict = {}
        cdef int points 
        points = len(sorted_points)
        #localdict = self.int_dict.get_multi([str(entry.x) for entry in sorted_points])
        localdict = {}
        for entry in sorted_points:
            localdict[str(entry[0])] = self[str(entry[0])] 
        
        if localdict is None:
            print 'Couldnt do get multi, result came back as none'
        #which is pretty fatal...

        cdef int x
        cdef int y
        cdef int ykey
        cdef float fpy 

        for p in sorted_points:
            x = p[0]
            y = p[1]
            ydict = localdict[str(x)] #dict {y: list of spectra id's}
            if ydict is None:
                print 'Fatal, no ydict for mass: ', x
                
            #ys = sorted(ydict.keys(), cmp=lambda xx,yy: y_compare(xx,yy,y))
            ys = ydict.keys()
            for ykey in ys:
                #fykey = float(ykey)
                ycomps = ydict[ykey]
                for comp in ycomps:
                    co = searchdict.get(comp, None)

                    if co is None:
                        co = {'score': 0, 'commons':{}}
                        searchdict[comp] = co
                    #fpy = float(y)
                    co['score'] += points  # bucket separation. 
                    co['commons'][x] = ykey #no need to worry about collision here
            points -= 1

        #return a dict of compounds
        #k = searchdict.keys()
        s = searchdict
        scored_compounds_list = searchdict.keys()#k #sorted(k, cmp=lambda x,y: int(s[x]['score']-s[y]['score']))
        scored_compounds_dict = {}
        for c in scored_compounds_list:
            sc = searchdict[c]['score']
            place = scored_compounds_dict.get(sc, None)
            if place is None:
                place = []
                scored_compounds_dict[sc] = place
            #possible that using a list here (place) is slower than using a dict (keyed on what? a set of commons?) 
            place.append({'commons': s[c]['commons'], 'compound': c})
        
        return scored_compounds_dict


#here we init the datahash.
#we cant do this in __init__ since the double import seems to cause 
#tokyo to block: an open filehandles thing perhaps?
def low_level_create(keyspace = 'default'):
    print 'enter create'
    if DATAHASH[0] == None:
        DATAHASH[0] = TokyoHash(keyspace=keyspace)    
    print 'create finished'

low_level_create()


