import six
# Python3 support, keep import hacks here

if six.PY3:
    from urllib.parse import parse_qs, urlparse, urlunparse, quote, \
                             urlsplit, urlencode, unquote
    from io import StringIO
else:
    try:
        from urllib.parse import parse_qs
    except ImportError:  # fall back for Python 2.5
        from cgi import parse_qs
    from urllib.parse import urlparse, urlunparse, urlsplit
    from urllib.parse import urlencode, unquote, quote
    from io import StringIO
