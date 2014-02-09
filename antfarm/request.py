
import cgi
from http.cookies import SimpleCookie
from io import StringIO
from urllib.parse import parse_qs

from .utils.functional import buffered_property

import logging
log = logging.getLogger(__name__)


class Request(object):
    def __init__(self, app, environ):
        self.app = app
        self.environ = environ
        self.path = self.environ.get('PATH_INFO', b'/')
        self.method = self.environ.get('REQUEST_METHOD')

        self.content_type, self.content_params = cgi.parse_header(environ.get('CONTENT_TYPE', ''))

    @buffered_property
    def raw_cookies(self):
        '''Raw access to cookies'''
        cookie_data = self.environ('HTTP_COOKIE', '')
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
        elif self.content_type == 'multipart/form-data':
            return cgi.parse_multipart(
                StringIO(self.body),
                self.content_params['boundary']
            )
        return {}
