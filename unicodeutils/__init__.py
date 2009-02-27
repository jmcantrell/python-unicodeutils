import csv, unicodedata, string
from StringIO import StringIO

ENCODING = 'utf-8'

def encode(value, encoding=None):
    if not encoding: encoding = ENCODING
    if value is None: return ''
    if isinstance(value, str): return value
    if is_list(value): return [encode(v, encoding) for v in value]
    if not isinstance(value, unicode): value = unicode(value)
    return value.encode(encoding)

def decode(value, encoding=None):
    if not encoding: encoding = ENCODING
    if value is None: return u''
    if isinstance(value, unicode): return value
    if is_list(value): return [decode(v, encoding) for v in value]
    if not isinstance(value, str): value = str(value)
    return unicode(value, encoding=encoding)

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
    """Test if value is a list or tuple.
    >>> is_list('foo')
    False
    >>> is_list(('this', 'is', 'a', 'tuple'))
    True
    >>> is_list(['this', 'is', 'a', 'list'])
    True
    """
    return isinstance(value, (list, tuple))

def listify(value):
    """Ensure that the value is a list.
    >>> listify('foo')
    ['foo']
    >>> listify(['foo', 'bar'])
    ['foo', 'bar']
    """
    return value if is_list(value) else [value]
