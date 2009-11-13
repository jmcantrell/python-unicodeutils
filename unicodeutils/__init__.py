import unicodedata, string

ENCODING = 'utf-8'

def encode(value, encoding=None):
    if not encoding: encoding = ENCODING
    if value is None: return ''
    if isinstance(value, str): return value
    if is_list(value): return list(encode(v) for v in value)
    if is_dict(value): return dict((encode(k), encode(v)) for k, v in value.items())
    if not isinstance(value, unicode): value = unicode(value)
    return value.encode(encoding)

def decode(value, encoding=None):
    if not encoding: encoding = ENCODING
    if value is None: return u''
    if isinstance(value, unicode): return value
    if is_list(value): return list(decode(v) for v in value)
    if is_dict(value): return dict((decode(k), decode(v)) for k, v in value.items())
    if not isinstance(value, str): value = str(value)
    return unicode(value, encoding)

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
    return value_new.strip(s)

def sanitize(value):
    return squeeze(normalize_symbols(normalize(strip_non_word(value))).lower().replace(' ', '_'), '_')

def is_list(value):
    return isinstance(value, (list, tuple))

def is_dict(value):
    return isinstance(value, dict)

def listify(value):
    return value if is_list(value) else [value]
