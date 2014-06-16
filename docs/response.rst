========
Response
========

The response module includes the Response class, and a number of utilities.

Response
========

.. class:: Response(content='', status_code=STATUS.OK, content_type='text/html')

   .. attribute:: encoding
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

   .. attribute:: status

      A helper to return the status code and message as a single string.

   .. method:: close()

      Attempts to close self.content if it has a callable close attribute.

      The WSGI spec requires it to call the close methon on response objects 
      which have one.  This method allows, for instance, passing a file as
      ``content`` and being sure it is closed.

Response sub-classes
--------------------

Additionally, there is a sub-class of Response for each HTTP Status code.

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

