
from collections import namedtuple

import re
import http

class KeepLooking(Exception):
    '''Used to tell a url_dispatcher to skip this pattern and keep looking.'''
    pass

# XXX If the number of regexes grows, it may be worth pre-compiling
class url(namedtuple('url', ('regex', 'view', 'kwargs',))

class url_dispatcher(object):
    def __init__(self, patterns):
        self.patterns = [
            url(*p) if not isinstance(p, url) else p
            for p in patterns
        ]

    def __call__(self, request):
        for pattern in self.patterns:
            m = pattern.regex.match(request.path)
            if m:
                try:
                    return pattern.view(request, **pattern.kwargs)
                except KeepLooking:
                    pass

        self.handle_not_found(request)

    def handle_not_found(self, request):
        raise http.NotFound()
