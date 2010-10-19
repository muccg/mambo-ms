CREATE OR REPLACE FUNCTION search_by_spectra(text, integer)
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
    tot_ml = len(l)
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

def main(xys, limit):
    querydict = create_querydict(xys)
    tot_mq = len(querydict)

    result_list = []
    compounds = plpy.execute("SELECT c.id, s.raw_points FROM mambomsapp_compound c JOIN mambomsapp_spectrum s ON c.id = s.compound_id")
    for c in compounds:
        sum_IqIl,sum_Iq2,sum_Il2,tot_cm,tot_ml = calculate_values(c, querydict)
        if tot_cm:
            A = float(tot_cm * tot_cm) / float(tot_mq * tot_mq)
            B = float(sum_IqIl * sum_IqIl) / float(sum_Iq2*sum_Il2)
            C = A*B

            if not result_list or (C > result_list[-1][0]):
                result_list.append( (C, c['id']) )
                result_list.sort(key=lambda x: x[0],reverse=True)
                result_list = remove_duplicates(result_list)
                while len(result_list) > limit:
                    result_list.pop()

    result = ""
    for score, id in result_list: 
        result += "%s %s\n" % (score, id)

    return result


return main(args[0].split(','),args[1])

$$ LANGUAGE plpythonu;

