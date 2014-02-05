
from unittest import TestCase, main

from antfarm import request

BASE_ENVIRON = {'REQUEST_METHOD': b'GET'}
class RequestTest(TestCase):


    def test_001_content_type(self):
        req = request.Request(BASE_ENVIRON)
        self.assertEqual(req.content_type, '')

        req = request.Request(dict(BASE_ENVIRON,
            CONTENT_TYPE='text/plain'.encode(request.DEFAULT_ENCODING),
        ))
        self.assertEqual(req.content_type, 'text/plain')

        req = request.Request(dict(BASE_ENVIRON,
            CONTENT_TYPE='text/plain; charset=utf-8'.encode(request.DEFAULT_ENCODING),
        ))
        self.assertEqual(req.content_type, 'text/plain')
        self.assertEqual(req.content_params['charset'], 'utf-8')

if __name__ == '__main__':
    main()