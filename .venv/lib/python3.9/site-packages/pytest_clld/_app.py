import json
import contextlib
import xml.etree.cElementTree as etree

import mock
import webtest
import html5lib
from webob.request import environ_add_POST


def _add_header(headers, name, value):
    """Add (name, value) to headers.

    >>> headers = []
    >>> assert _add_header(headers, 'n', 'v') == [('n', 'v')]
    >>> headers = {}
    >>> assert _add_header(headers, 'n', 'v') == {'n': 'v'}
    """
    if isinstance(headers, dict):
        headers[name] = str(value)
    else:  # pragma: no cover
        headers.append((name, str(value)))


class ExtendedTestApp(webtest.TestApp):
    """WebTest TestApp with extended support for evaluation of responses."""

    parsed_body = None

    _add_header = staticmethod(_add_header)

    def get(self, *args, **kw):
        kw.setdefault('headers', {})
        if kw.pop('xhr', False):
            self._add_header(kw['headers'], 'x-requested-with', 'XMLHttpRequest')
        accept = kw.pop('accept', False)
        if accept:
            self._add_header(kw['headers'], 'accept', accept)
        kw.setdefault('status', 200)
        body_parser = kw.pop('_parse_body', None)
        res = super(ExtendedTestApp, self).get(*args, **kw)
        if body_parser and res.status_int < 300:
            self.parsed_body = body_parser(res.body)
        return res

    def get_html(self, *args, **kw):
        docroot = kw.pop('docroot', None)
        res = self.get(*args, _parse_body=html5lib.parse, **kw)
        child_nodes = list(self.parsed_body)
        assert child_nodes
        if docroot:
            for e in child_nodes[1]:
                assert e.tag.endswith(docroot)
                break
        return res

    def get_json(self, *args, **kw):
        _loads = lambda s: json.loads(str(s, encoding='utf8'))
        return self.get(*args, _parse_body=_loads, **kw)

    def get_xml(self, *args, **kw):
        return self.get(*args, _parse_body=etree.fromstring, **kw)

    def get_dt(self, _path, *args, **kw):
        if 'sEcho=' not in _path:
            sep = '&' if '?' in _path else '?'
            _path = _path + sep + 'sEcho=1'
        kw.setdefault('xhr', True)
        return self.get_json(_path, *args, **kw)


class Route(mock.Mock):
    """Mock a pyramid Route object."""

    def __init__(self, name='home'):
        super(Route, self).__init__()
        self.name = name


def _set_request_property(req, k, v):
    if k == 'is_xhr':
        req.environ['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest' if v else ''
    elif k == 'params':
        environ_add_POST(req.environ, v)
    elif k == 'matched_route':
        setattr(req, k, Route(v))
    else:  # pragma: no cover
        setattr(req, k, v)


@contextlib.contextmanager
def request(env, **props):
    _cache = {}
    for k, v in props.items():
        _cache[k] = getattr(env['request'], k, None)
        _set_request_property(env['request'], k, v)

    yield env['request']

    for k, v in _cache.items():
        _set_request_property(env['request'], k, v)
    env['request'].environ.pop('HTTP_X_REQUESTED_WITH', None)
    environ_add_POST(env['request'].environ, {})


@contextlib.contextmanager
def utility(env, utility, interface):
    env['registry'].registerUtility(utility, interface)
    yield
    env['registry'].unregisterUtility(utility, interface)
