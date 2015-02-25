=======
Request
=======

The ``Request`` class encapsulates a request, as well as providing commonly
needed parsing, such as cookies, querystrings, and body.


.. class:: Request(app, environ)

   .. attribute:: path

      The requested URI

   .. attribute:: method

      The HTTP Verb used in this request (e.g. GET, POST, OPTIONS, etc)

   .. attribute:: content_type

      The supplied content type of this request.

   .. attribute:: content_params

      A dict containing any additional parameters passed in the content type
      header.

   .. attribute:: raw_cookies

      A SimpleCookie object.

   .. attribute:: cookies

      A simpler interface to raw_cookies, which is a dict of cookie names to
      values.

   .. attribute:: body

      The raw contents of the request body.

   .. attribute:: query_data

      A dict of data parsed from the query string.

   .. attribute:: request_data

      If the request content is a HTTP Form, returns the parsed data.


The following attributes are lazy, and only parsed when accessed:

- raw_cookies
- cookies (reads raw_cookies)
- query_data
- body
- request_data (reads body)
