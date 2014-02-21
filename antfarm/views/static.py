
'''
Helper for serving static content.

'''
import os.path

from antfarm import response
import mimetypes

class ServeStatic(object):
    def __init__(self, root):
        self.root = root

    def __call__(self, request, path):
        full_path = os.path.abspath(os.path.join(self.root, path))
        if not full_path.startswith(self.root):
            return response.NotFound()

        # Guess content type
        content_type, encoding = mimetypes.guess_type(full_path)
        content_type = content_type or 'application/octet-stream'

        try:
            fin = open(full_path, 'rb')
        except FileNotFoundError:
            return response.NotFound()

        return response.Response(iter(fin), content_type=content_type)
