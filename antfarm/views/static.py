
'''
Helper for serving static content.

'''
from antfarm import http
import mimetypes

class ServeStatic(object):
    def __init__(self, root):
        self.root = root

    def __call__(self, path):
        full_path = os.path.absdir(os.path.join(self.root, path))
        if not full_path.startswith(self.root):
            return http.NotFound()

        # Guess content type
        content_type, encoding = mimetypes.guess_type(full_path)
        content_type = content_type or 'application/octet-stream'

        return http.Response(iter(open(full_path, 'rb')),
            content_type=content_type
        )
