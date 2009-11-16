import unicodedata, string

ENCODING = 'utf-8'

def encode(value, encoding=ENCODING): #{{{1
    """Make sure that the given value is a string or contains strings.
    >>> encode(u'foo')
    'foo'
    >>> encode('foo')
    'foo'
    >>> encode([u'foo', [u'bar', u'baz']])
    ['foo', ['bar', 'baz']]
    >>> encode({u'foo': [u'bar', u'baz']})
    {'foo': ['bar', 'baz']}
    """
    # None is treated as an empty string
    if value is None: return ''
    # If already a string, no need to encode
    if isinstance(value, str): return value
    # If list/tuple, recursively encode
    if is_list(value): return list(encode(v) for v in value)
    # If dict, recursively encode keys and values
    if is_dict(value): return dict((encode(k), encode(v)) for k, v in value.items())
    # Make absolutely sure that value is unicode
    if not isinstance(value, unicode): value = unicode(value)
    return value.encode(encoding)

def decode(value, encoding=ENCODING): #{{{1
    """Make sure that the given value is unicode or contains unicode.
    >>> decode('foo')
    u'foo'
    >>> decode(u'foo')
    u'foo'
    >>> decode(['foo', ['bar', 'baz']])
    [u'foo', [u'bar', u'baz']]
    >>> decode({'foo': ['bar', 'baz']})
    {u'foo': [u'bar', u'baz']}
    """
    # None is treated as an empty string
    if value is None: return u''
    # If already unicode, no need to decode
    if isinstance(value, unicode): return value
    # If list/tuple, recursively decode
    if is_list(value): return list(decode(v) for v in value)
    # If dict, recursively decode keys and values
    if is_dict(value): return dict((decode(k), decode(v)) for k, v in value.items())
    # Make absolutely sure that value is a string
    if not isinstance(value, str): value = str(value)
    return unicode(value, encoding)

def strip_non_word(value, replace=None, allowed=None): #{{{1
    """Remove any non-word characters from a string.
    >>> strip_non_word('foo.bar?baz')
    u'foo bar baz'
    """
    pool = string.letters + string.digits + u'-_ ' + (allowed or '')
    return u''.join(map(lambda s: (s in pool and s) or (replace or u' '), value))

def strip_non_ascii(value, replace=None): #{{{1
    """Remove any non-ascii characters from a string.
    >>> strip_non_ascii(u'a\xe4\xf6\xfcb')
    u'a   b'
    """
    return u''.join(map(lambda s: (s <= u'~' and s) or (replace or u' '), value))

def strip_non_windows(value, replace=None): #{{{1
    """Removes any characters that are not allowed in Windows filenames.
    >>> strip_non_windows('foo:bar?baz')
    u'foo bar baz'
    """
    return u''.join(map(lambda s: (s not in u':*?;"<>|' and s) or (replace or u' '), value))

def normalize(value): #{{{1
    """Get an ascii approximaton of a string containing special characters.
    >>> normalize(u'\xe4\xf6\xfc')
    u'aou'
    """
    return unicode(unicodedata.normalize('NFKD', value).encode('ascii', 'ignore'), encoding='utf-8')

def normalize_symbols(value): #{{{1
    xlate = {'&': 'and'}
    for symbol, replace in xlate.iteritems():
        value = value.replace(symbol, replace)
    return value

def squeeze(value, s=' '): #{{{1
    """Remove excessive characters.
    >>> squeeze('   foo   bar  baz  ')
    'foo bar baz'
    >>> squeeze('foo__bar___baz__', '_')
    'foo_bar_baz'
    """
    value_new = value
    ss = s*2
    while True:
        if ss not in value_new: break
        value_new = value_new.replace(ss, s)
    return value_new.strip(s)

def sanitize(value): #{{{1
    """Produce a super-safe version of a string.
    >>> sanitize(u' F\xf6\xf6.bar  baz.  ')
    u'foo_bar_baz'
    """
    return squeeze(normalize_symbols(strip_non_word(normalize(value.replace('.', ' ')))).lower().replace(' ', '_'), '_')

def is_list(value): #{{{1
    return isinstance(value, (list, tuple))

def is_dict(value): #{{{1
    return isinstance(value, dict)

def listify(value): #{{{1
    return value if is_list(value) else [value]
