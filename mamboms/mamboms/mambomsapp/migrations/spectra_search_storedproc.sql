BEGIN;
CREATE PROCEDURAL LANGUAGE plpythonu;
ALTER PROCEDURAL LANGUAGE plpythonu OWNER TO postgres;
COMMIT;

BEGIN;
CREATE OR REPLACE FUNCTION search_by_spectra(text, integer, integer, integer[])
    RETURNS text
AS $$

def round(f):
    if( (f-int(f) < 0.7) and (f - int(f)) >= -0.3):
        return int(f)
    else:
        return int(f)+1

def create_querydict(xys):
    dict = {}
    for x,y in zip(xys[::2], xys[1::2]):
        key = str(round(float(x))) 
        prev_y = dict.get(key)
        if prev_y is None:
            dict[key] = float(y)
        else:
            dict[key] = (prev_y+float(y))/2

    return dict

def calculate_values(compound, querydict):
    sum_IqIl = sum_Iq2 = sum_Il2 = tot_cm = 0
    #l = [int(s) for s in c['raw_points'].split(',')]
    l = compound['raw_points'].split(',')
    tot_ml = len(l) / 2
    for x,y in zip(l[::2],l[1::2]):
        query_y = querydict.get(x)
        if query_y is not None:
            iy = int(y)
            # for common x values
            sum_IqIl += (query_y * iy)
            sum_Iq2 += (query_y * query_y)
            sum_Il2 += (iy * iy)
            tot_cm += 1
    return sum_IqIl,sum_Iq2,sum_Il2,tot_cm,tot_ml

def remove_duplicates(sorted_result_list):
    '''Remove the duplicates (according to the id) with smaller values 
       from a sorted list'''
    result_list = []
    seen = set()
    for result in sorted_result_list:
        if result[1] in seen: 
            continue
        result_list.append(result)
        seen.add(result[1])
    return result_list

def main(xys, limit, adjust, dataset_ids):
    querydict = create_querydict(xys)
    tot_mq = len(querydict)

    result_list = []
    where_clause = ""
    if len(dataset_ids) > 0:
        '''It appears that even though we have specified the dataset ids to be integer[], they
           actually end up coming through as a string. So rather than using the where clause below, 
           we just use one that chops the [ and ] off the list.'''
        '''where_clause = "WHERE c.dataset_id in (%s)" % (",".join([str(x) for x in dataset_ids]))'''
        where_clause = "WHERE c.dataset_id in (%s)" % (dataset_ids[1:-1])

    
        compounds = plpy.execute("SELECT c.id, s.raw_points FROM mambomsapp_compound c JOIN mambomsapp_spectrum s ON c.id = s.compound_id %s" % (where_clause))
        for c in compounds:
            sum_IqIl,sum_Iq2,sum_Il2,tot_cm,tot_ml = calculate_values(c, querydict)
            if tot_cm:
                B = float(sum_IqIl * sum_IqIl) / float(sum_Iq2*sum_Il2)
                C = 0
                if adjust:
                    A = float(tot_cm * tot_cm) / float(tot_mq * tot_ml)
                    C = A*B
                else:
                    C = B

                if not result_list or (C >= result_list[-1][0]):
                    result_list.append( (C, c['id']) )
                    result_list.sort(key=lambda x: x[0],reverse=True)
                    result_list = remove_duplicates(result_list)
                    while len(result_list) > limit:
                        result_list.pop()

    result = ""
    for score, id in result_list: 
        result += "%s %s\n" % (score, id)

    return result


return main(args[0].split(','),args[1], args[2], args[3])

$$ LANGUAGE plpythonu;

COMMIT;

