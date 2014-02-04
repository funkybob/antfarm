===========
HTTP Module
===========

This module include helpers for HTTP responses.

STATUS_CODES
============

A tuple of two-tuples, each of (status code, status message)

STATUS
======

An OrderedDict sub-class constructed from STATUS_CODES.

Additionally, the status codes can be accessed by name.

For example:

.. code-block:: python

    >>> STATUS.OK
    200

    >>> STATUS[200]
    'OK'

Response
========

.. class:: Response(content='', status=STATUS.OK, content_type='text/html')

   .. attribute:: content_encoding
   .. attribute:: status_message

   .. attribute:: headers

      A dict of HTTP headers

   .. attribute:: cookies

      A SimpleCookie container for resposne cookies.

   .. method:: add_cookie(key, value, \**kwargs)

      Add a cookie to the response.

      If only key and value are passed, then dict access to self.cookies is
      used.  Otherwise, a Morsel is instanciated, and the key, value and kwargs
      passed to its set method.  Then it's added to the cookies container.

   .. method:: get_status()

      Helper method to return the status code and message as a single string.

Response sub-classes
--------------------

Additionally, there is a sub-class of Response for each HTTP Status code.

