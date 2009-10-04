import csv, unicodedata, string
from StringIO import StringIO

ENCODING = 'utf-8'

def recode(value, src, dst, encoding=None):
    if not encoding: encoding = ENCODING
    if value is None: return dst()
    if isinstance(value, dst): return value
    if is_list(value): return list(dst(v, encoding) for v in value)
    if is_dict(value): return dict((dst(k), dst(v)) for k, v in value.items())
    if not isinstance(value, src): value = src(value)
    return dst(value, encoding=encoding)

def encode(value, encoding=None):
    return recode(value, unicode, str, encoding)

def decode(value, encoding=None):
    return recode(value, str, unicode, encoding)

def strip_non_word(value, replace=None, allowed=''):
    if replace is None: replace = u'_'
    pool = string.letters + string.digits + u'-_ ' + allowed
    return u''.join(map(lambda s: (s in pool and s) or replace, value))

def strip_non_ascii(value, replace=None):
    if replace is None: replace = u'_'
    return u''.join(map(lambda s: (s <= u'~' and s) or replace, value))

def strip_non_windows(value, replace=None):
    if replace is None: replace = u'_'
    return u''.join(map(lambda s: (s not in u':*?;"<>|' and s) or replace, value))

def normalize(value):
    return unicode(unicodedata.normalize('NFKD', value).encode('ascii', 'ignore'), encoding='utf-8')

def normalize_symbols(value):
    xlate = {'&': 'and'}
    for symbol, replace in xlate.iteritems():
        value = value.replace(symbol, replace)
    return value

def squeeze(value, s):
    value_new = value
    ss = s*2
    while True:
        if ss not in value_new: break
        value_new = value_new.replace(ss, s)
    return value_new

def sanitize(value):
    return squeeze(normalize_symbols(normalize(strip_non_word(value))).lower().replace(' ', '_'), '_')

def is_list(value):
    return isinstance(value, (list, tuple))

def is_dict(value):
    return isinstance(value, dict)

def listify(value):
    return value if is_list(value) else [value]
