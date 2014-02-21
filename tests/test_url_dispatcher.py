from functools import partial
from unittest import TestCase, main

from antfarm.request import Request
from antfarm.response import (Response, NotFound, ResponseError, Created,
                              OK, Accepted)
from antfarm.urls import url_dispatcher, URL, KeepLooking


def test_view(request, slug=None, direction=None):
    if direction == 1:
        return Created(str(direction))
    elif direction == -1:
        raise KeepLooking
    if slug is not None:
        return Accepted(str(slug))
    return OK('OK')


class UrlDispatcherTest(TestCase):
    def setUp(self):
        self.patterns = [
            (r'^/$', test_view),
            (r'^/up/$', partial(test_view, slug=None, direction=1)),
            (r'^/down/$', partial(test_view, slug=None, direction=-1)),
            (r'^/(?P<slug>[-\w]+)/$', test_view),
        ]
        self.instance = url_dispatcher(*self.patterns)
        self.environ = {'REQUEST_METHOD': 'GET'}

    def test_001_making_url_instances(self):
        self.assertEqual(len(self.patterns), 4)

        for original, result in zip(self.patterns, self.instance.patterns):
            self.assertIsInstance(result, URL)
            self.assertEqual(original[0], result.regex.pattern)

    def test_002_not_found(self):
        req = Request(None, self.environ)
        req.path = '/abc/def/'
        applied = self.instance(req)
        self.assertEqual(applied.status_code, 404)
        # check for ResponseError because it is the separating point between
        # Response and NotFound
        self.assertIsInstance(applied, ResponseError)
        self.assertIsInstance(applied, NotFound)

    def test_003_root(self):
        req = Request(None, self.environ)
        req.path = '/'
        applied = self.instance(req)
        self.assertEqual(applied.status_code, 200)
        self.assertIsInstance(applied, Response)
        self.assertEqual(applied.content, 'OK')

    def test_004_partial(self):
        req = Request(None, self.environ)
        req.path = '/up/'
        applied = self.instance(req)
        self.assertEqual(applied.status_code, 201)
        self.assertIsInstance(applied, Created)
        self.assertEqual(applied.content, '1')

    def test_005_capturing_kwargs(self):
        req = Request(None, self.environ)
        req.path = '/random-slug/'
        applied = self.instance(req)
        self.assertEqual(applied.status_code, 202)
        self.assertIsInstance(applied, Accepted)
        self.assertEqual(applied.content, 'random-slug')

    def test_006_keep_looking(self):
        req = Request(None, self.environ)
        req.path = '/down/'
        applied = self.instance(req)
        # KeepLooking should be raised, so we end up with the Accepted
        # response.
        self.assertEqual(applied.status_code, 202)
        self.assertIsInstance(applied, Accepted)
        self.assertEqual(applied.content, 'down')


if __name__ == '__main__':
    main()
