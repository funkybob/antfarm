
class With(object):
    '''
    Decorator factory for wrapping a view with a context manager.
    '''
    def __init__(self, outer, *args, **kwargs):
        self.outer = outer
        self.args = args
        self.kwargs = kwargs

    def __call__(self, inner):
        @wraps(inner)
        def _inner(request, *args, **kwargs):
            with self.outer(request, *self.args, **self.kwargs) as request:
                return inner(request, *args, **kwargs)

