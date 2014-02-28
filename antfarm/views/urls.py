'''
Django-style URL dispatcher view.

    App(root_url=url_dispatcher(
        (r'^/$', views.index),
        (re.compile(r'^/(?P<foo>\d+)/'), views.detail, {'bar': True}),
    )

The view will be called with the request, and any matched _named_ groups.
Extra kwargs can be passed as a 3rd positional argument.

There is a namedtuple class defined called URL provided.  All patterns will be
assembled as a URL instance, and their regex compiled.  If kwargs are not
specified, they will default to {}.
'''

from collections import namedtuple
from functools import partial
import re

from . import response

class KeepLooking(Exception):
    '''Used to tell a url_dispatcher to skip this pattern and keep looking.'''
    pass

URL = namedtuple('url', ('regex', 'view'))

class url_dispatcher(object):
    __slots__ = ('patterns',)

    def __init__(self, *patterns):
        self.patterns = [self._make_url(pattern) for pattern in patterns]

    def _make_url(self, pattern):
        '''Helper to ensure all patterns are url instances.'''
        return URL(re.compile(pattern[0]), pattern[1])

    def __call__(self, request, *args, **kwargs):
        path = getattr(request, 'remaining_path', request.path)
        for pattern in self.patterns:
            m = pattern.regex.match(path)
            if m:
                request.remaining_path = path[m.end():]
                kwargs.update(m.groupdict())
                try:
                    return pattern.view(request, *args, **kwargs)
                except KeepLooking:
                    pass

        return self.handle_not_found(request)

    def handle_not_found(self, request):
        return response.NotFound()

    def register(self, pattern, view=None):
        '''Allow decorator-style construction of URL pattern lists.'''
        if view is None:
            return partial(self.register, pattern)
        self.patterns.append(self._make_url((pattern, view)))
        return view
