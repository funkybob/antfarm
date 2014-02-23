from unittest import TestCase, main
from antfarm.response import MethodNotAllowed, MovedPermanently, Response


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

    def test_004_status_code_fallback(self):
        response = Response()
        self.assertIsNotNone(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_005_status_code_given(self):
        # no validation is currently done on the status code.
        response = Response(status_code=999)
        self.assertIsNotNone(response.status_code)
        self.assertEqual(response.status_code, 999)

    def test_006_custom_status(self):
        response = Response(status_code=999,
                            status_message="call the emergency services")
        self.assertEqual(response.status, '999 call the emergency services')
        self.assertEqual(response.status_code, 999)
        self.assertEqual(response.status_message, "call the emergency services")

    def test_007_add_cookie(self):
        response = Response()
        self.assertEqual(len(response.cookies), 0)
        response.add_cookie(key='test', value='a test!')
        self.assertEqual(len(response.cookies), 1)


if __name__ == '__main__':
    main()
