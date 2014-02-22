from unittest import TestCase, main
from antfarm.response import MethodNotAllowed


class ResponseTest(TestCase):

    def test_001_method_not_allowed(self):
        response = MethodNotAllowed(permitted_methods=('POST', 'PUT'))
        self.assertEqual(response.headers['Allow'], 'POST, PUT')


if __name__ == '__main__':
    main()
