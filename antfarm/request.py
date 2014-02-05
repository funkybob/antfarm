
from http.cookies import SimpleCookie
from urllib.parse import parse_qs

from .utils.functional import buffered_property

import logging
log = logging.getLogger(__name__)

DEFAULT_ENCODING = 'ISO-8859-1'

class Request(object):
    def __init__(self, environ):
        self.environ = environ
        self.path = self.envstr('PATH_INFO', b'/')
        self.method = self.envstr('REQUEST_METHOD')

        self.content_type, self.content_params = self.parse_content_type()

    def envstr(self, key, default=b''):
        '''Retrieve a string from the environ, decoded correctly.'''
        return self.environ.get(key, default).decode(DEFAULT_ENCODING)

    @buffered_property
    def raw_cookies(self):
        '''Raw access to cookies'''
        cookie_data = self.envstr('HTTP_COOKIE')
        if not cookie_data:
            return {}
        cookies = SimpleCookie()
        cookies.load(cookie_data)
        return cookies

    @buffered_property
    def cookies(self):
        '''Simplified Cookie access'''
        return {
            key: self.raw_cookies[key].value
            for key in self.raw_cookies.keys()
        }

    @buffered_property
    def query_data(self):
        return parse_qs(
            self.environ.get('QUERY_STRING', ''),
            keep_blank_values=True
        )

    @buffered_property
    def body(self):
        size = int(self.environ.get('CONTENT_LENGTH', 0))
        if not size:
            return ''
        return self.environ['wsgi.input'].read(size)

    @buffered_property
    def request_data(self):
        if self.content_type == 'application/x-www-form-urlencoded':
            return parse_qs(self.body)
        # Support multi-part

    def parse_content_type(self):
        ctype = self.envstr('CONTENT_TYPE')
        content_type, _, params = ctype.partition(';')
        content_params = {}
        for param in params.split(';'):
            k, _, v = param.strip().partition('=')
            content_params[k] = v
        return content_type, content_params
