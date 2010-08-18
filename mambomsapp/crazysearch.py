from mamboms.mambomsapp.models import Dataset, Compound, PointSet, Spectrum
import time
import gc
import search_datastructures as sd
from django.http import HttpResponse

def numeric_compare(x,y):
    '''just a compare function for sorting, since it needs to return an int'''
    if x>y:
       return 1
    elif x==y:
       return 0
    else: # x<y
       return -1

def build_compound_hash(c):
    r = {}
    for pp in c:
        r[pp[0]] = pp[1]
    return r

def print_scored(s):
    for score in s.keys():
        print "SCORE: ", score
        for ss in s[score]:
            print ss['commons']

def compute_bucket(qdict, bucket):
    r = []
    total = 0.0
    for e in bucket:
        n = sd.compute_comparison(e['commons'], qdict, e['commons'].keys())
        r.append( (n,e) )
        total += n

    #compute stats
    r.sort(cmp=numeric_compare, reverse = True )


    return r[0][0], r[len(r)-1][0], total, r[0][1]['compound'], r[len(r)-1][1]['compound'], [[i[0],i[1]['compound']] for i in r[:10]]


def pTest(i, thresh=1.0):
    import profile
    profile.run('test(%d, thresh=%f)' % (i, thresh))


def test(i, thresh=1.0):
    po = Compound.objects.get(id=i).point_set.get_rounded()
    a = [(p.x,p.y) for p in po]

    t0 = time.time()
    s = sd.DATAHASH[0].find_matches(a)
    total_time = time.time() - t0
    
    k = s.keys()
    k.sort(reverse=True)
    top_ten = []
    qdict = build_compound_hash(a)
    count =0
    for kk in k[:int(thresh*len(k))]:
        t = time.time()
        c = s[kk]
        high, low, total, best, worst, bucket_ten = compute_bucket(qdict, c)
        
        for b in bucket_ten:
            b.append(count)
            b.append(kk)


        top_ten += bucket_ten
        top_ten.sort(cmp=numeric_compare, reverse=True)
        top_ten = top_ten[:10]
        count += 1

    print '%d buckets.' % (len(k))

    print 'Top Ten: '
    for compscore in top_ten:
        comp = Spectrum.objects.get(id=compscore[1]).compound
        print '%f : %s (%s) [bucket %s [score: %s]]' % (compscore[0] * 100, comp.cas_name, comp.link_to_graph(), str(compscore[2]), str(compscore[3]) )

    print 'find_matches: ', total_time   
    print 'total time: ', time.time() - t0

def create_hash(request, qset=None, limit=None, keyspace = 'default'):
    print 'enter create'
    if sd.DATAHASH[0] == None:
        sd.DATAHASH[0] = sd.TokyoHash(keyspace=keyspace) 
    return HttpResponse('create done')

def build_hash(request, qset = None, limit = None):
    if sd.DATAHASH[0] is None or sd.DATAHASH[0].state != sd.DATAHASH[0].STATE_BUILDING:
        print 'building datahash, limit is %s' % (str(limit))
        sd.DATAHASH[0]._build(Spectrum.objects.all())
        return HttpResponse('build done')
    else:
        return HttpResponse('build already in progress')

def status(request, *args):
    if sd.DATAHASH[0] == None:
        return HttpResponse("Not created") 
    d = sd.DATAHASH[0].status()
    s = ""
    for k in d.keys():
        s += "%s : %s<br>" % (str(k), str(d[k]))
    return HttpResponse(s)

def search(xys, thresh = 1.0, *args):
    '''expects a stream of x y values'''
    
    #Take [x1,y1,x2,y2,x3,y3] and turn it into
    #     [(x1,y1),(x2,y2),(x3,y3)]
    po = xys.get_rounded()
    #a = zip(xys[::2], xys[1::2])
    a = [(p.x, p.y) for p in po]

    t0 = time.time()
    s = sd.DATAHASH[0].find_matches(a)
    total_time = time.time() - t0

    k = s.keys()
    k.sort(reverse=True)
    print 'sorted =', k
    top_ten = []
    qdict = build_compound_hash(a)
    count =0
    for kk in k: #[:int(thresh*len(k))]:
        t = time.time()
        c = s[kk]
        high, low, total, best, worst, bucket_ten = compute_bucket(qdict, c)
        
        for b in bucket_ten:
            b.append(count)
            b.append(kk)


        top_ten += bucket_ten
        top_ten.sort(cmp=numeric_compare, reverse=True)
        top_ten = top_ten[:10]
        count += 1
    print '%d buckets.' % (len(k))
    print 'Top Ten: '
    
    retcomps = []
    for compscore in top_ten:
        try:
            comp = Spectrum.objects.get(id=compscore[1]).compound
            print '%f : %s (%s) [bucket %s [score: %s]]' % (compscore[0] * 100, comp.cas_name, comp.link_to_graph(), str(compscore[2]), str(compscore[3]) )
            retcomps.append( (compscore[0], comp.id) )
        except Exception, e:
            print 'Error for compound %d: %s' % (compscore[1], e)
        
    print 'find_matches: ', total_time   
    print 'total time: ', time.time() - t0

    return retcomps 

