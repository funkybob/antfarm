from unittest import TestCase, main
from antfarm.response import MethodNotAllowed, MovedPermanently


class ResponseTest(TestCase):

    def test_001_method_not_allowed(self):
        response = MethodNotAllowed(permitted_methods=('POST', 'PUT'))
        self.assertEqual(response.headers['Allow'], 'POST, PUT')
        self.assertEqual(response.status_code, 405)

    def test_002_redirect_allowed_schemes_ok(self):
        in_url = 'https://example.com/'
        response = MovedPermanently(location=in_url)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.headers['Location'], in_url)
        self.assertEqual(response.url, in_url)

    def test_003_redirect_invalid_scheme(self):
        with self.assertRaises(ValueError):
            MovedPermanently(location='ftp://example.com/')


if __name__ == '__main__':
    main()
