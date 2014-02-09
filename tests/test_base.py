
from unittest import TestCase, main

from antfarm import App, Response
from antfarm.response import STATUS

BASE_ENV = {
    'REQUEST_METHOD': 'GET',
}

class AppTest(TestCase):

    def test_001_basic(self):
        app = App(root_view=lambda r: Response('true'))

        def start_response(s, h):
            self.assertEqual(s, '200 OK')
            self.assertTrue(any(h[0] == 'Content-Type' for h in  h))

        resp = app(BASE_ENV, start_response)

        self.assertEqual(list(resp), [b'true'])

if __name__ == '__main__':
    main()
