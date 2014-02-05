

import logging
log = logging.getLogger(__name__)

from .request import Request

class App(object):
    '''
    Base Application class.

    Create an instance of this, passing configuration options, and use the resulting instance as your WSGI application callable.

        application = App(root_view=myview)

    You can also sub-class this to provide the root_view.
    '''
    def __init__(self, **opts):
        self.root_view = opts['root_view']
        self.opts = opts

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.root_view(request)

        headers = list(response.headers.items()) + [
            ('Set-Cookie', cookie.OutputString())
            for cookie in response.cookies.values()
        ]

        start_response(response.status, headers)
        # XXX Handle generator responses
        return [
            response.content.encode(response.content_encoding)
        ]
