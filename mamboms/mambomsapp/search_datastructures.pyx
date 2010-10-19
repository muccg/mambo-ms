import time
import gc
from pytc import *
import cPickle
#import cjson
import os
import settings

#limits on how many records to import
chunk_size = 2000
#records = 10000

DATAHASH = [None]

def compute_comparison(l_dict, q_dict, common_masses):
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
        self.local_dict = {}
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
            print 'Disk hash did not exist, creating new'
            self.int_dict.open(hashfile, HDBOWRITER | HDBOCREAT )
        else:
            print 'Disk hash already existed.'
            self.int_dict.open(hashfile, HDBOWRITER )
            
        self.chunk_size = chunk_size
        self.records = 0

        print 'TokyoHash init finished'
        #self._build(recordset)

    def status(self):
        if self.records > 0:
            perc = 100.0 * self.specs / float(self.records) 
        else:
            perc = 0
        self.stats['percentage'] = perc
        st = 'unknown'
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
        self.stats['actual_record_count'] = self.specs
        self.stats['keys'] = len(self.int_dict.keys())

        return self.stats

    def accumulate(self, recordset):
        l = self.local_dict
        self.state = self.STATE_BUILDING
        for spec in recordset:
            self.specs += 1
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

                l[x][y].append(int(spec.id)) #cast to int rather than use reference to db object
            #del(points)

        self.state = self.STATE_CLEAN
     
    def push(self):
        l = self.local_dict
        #now push it all to memcache
        import sys
        try:
            for k in l.keys():
                v = l[k]
                if sys.getsizeof(v) > 1000000:
                    print 'value for %s was too big' % (str(k)) 
                self[k] = l[k]


        except Exception, e:
            print 'Could not do a set: ', e


    def _build(self, recordset, limit = None):
        if self.state == self.STATE_BUILDING:
            return

        self.state = self.STATE_BUILDING
        self.build_start_time = time.time()
        low = 0
        finished = False
        l = self.int_dict
        if limit is None:
            self.records = recordset.count()
        else:
            self.record = limit
        while low <= self.records:
            cc = recordset 
            a = time.time()
            c = cc[low:low+chunk_size]
            
            self.accumulate(c)
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
        self.push()

        #write to stats
        self.stats['build'] = time.time()-self.build_start_time
        self.state = self.STATE_CLEAN

    def __getitem__(self, key):
        #v = self.int_dict[key]
        #return [(k, v[k]) for k in v.keys()]
        try:
            return cPickle.loads(self.int_dict.get(str(key)))
        except Exception, e:
            print '__getitem__ fail: ', e
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
