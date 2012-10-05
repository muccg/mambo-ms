from django.http import HttpResponse
from django.utils import simplejson
import decimal

def int_param(req_params, name, default=None):
    intval = default
    try:
        intval = int(req_params.get(name))
    except TypeError:
        # no value or not an int
        pass
    return intval

def decimal_param(req_params, name, default=None, max_digits=10):
    raw_value = req_params.get(name)
    if not raw_value:
        return default
    decimalval = default
    # extract possible sign
    sign = ''
    if raw_value[0] == '-':
        sign = '-'
        raw_value = raw_value[1:]
    # if greater than max_digits use the largest allowed value 
    if len(raw_value) > max_digits:
        raw_value = '9' * max_digits

    raw_value = sign + raw_value
    try:
        decimalval = decimal.Decimal(raw_value)
    except:
        # not a valid decimal
        pass
    return decimalval

def json_encode(str):
    encoder = simplejson.JSONEncoder()
    return encoder.encode(str)

def json_decode(str):
    decoder = simplejson.JSONDecoder()
    return decoder.decode(str)

