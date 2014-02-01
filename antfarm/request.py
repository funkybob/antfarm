
from http.cookies import SimpleCookie
from urllib.parse import parse_qs

import logging
log = logging.getLogger(__name__)

DEFAULT_ENCODING = 'ISO-8859-1'

class Request(object):
    def __init__(self, environ):
        self.environ = environ
        # XXX Handle encoding
        self.path = environ.get('PATH_INFO', '/')
        self.method = environ['REQUEST_METHOD']

        self.content_type, self.content_params = self.parse_content_type()
        self.cookies = self.parse_cookies()
        self.data = self.parse_query_data()

    def parse_cookies(self):
        cookies = self.environ.get('HTTP_COOKIE', '')
        if cookies == '':
            return {}
        else:
            c = SimpleCookie()
            c.load(cookies)
            return {
                key: c.get(key).value
                for key in c.keys()
            }

    def parse_query_data(self):
        if self.method == 'GET':
            return parse_qs(self.environ.get('QUERY_STRING', ''))
        elif self.method == 'POST':
            # Should test content type
            size = int(self.environ.get('CONTENT_LENGTH', 0))
            if not size:
                return {}
            return parse_qs(self.environ['wsgi.input'].read(size))

    def parse_content_type(self):
        content_type, _, params = self.environ.get('CONTENT_TYPE', '').partition(';')
        content_params = {}
        for param in params.split(';'):
            k, _, v = param.strip().partition('=')
            content_params[k] = v
        return content_type, content_params
