
from http.cookies import SimpleCookie, Morsel
import re
from urllib.parse import urlparse
from collections import OrderedDict

DEFAULT_ENCODING = 'ISO-8859-1'

STATUS_CODES = (
    (100, 'Continue'),
    (101, 'Switching Protocols'),

    (200, 'OK'),
    (201, 'Created'),
    (202, 'Accepted'),
    #(203, Non-Authoritative Information),
    (204, 'No Content'),
    (205, 'Reset Content'),
    (206, 'Partial Content'),

    (300, 'Multiple Choices'),
    (301, 'Moved Permanently'),
    (302, 'Found'),
    (303, 'See Other'),
    (304, 'Not Modified'),
    (305, 'Use Proxy'),
    #306 Deprecated
    (307, 'Temporary Redirect'),
    (308, 'Permanent Redirect'),

    (400, 'Bad Request'),
    (401, 'Unauthorized'),
    (402, 'Payment Required'),
    (403, 'Forbidden'),
    (404, 'Not Found'),
    (405, 'Method Not Allowed'),
    (406, 'Not Acceptable'),
    (407, 'Proxy Authentication Required'),
    (408, 'Request Timeout'),
    (409, 'Conflict'),
    (410, 'Gone'),
    (411, 'Length Required'),
    (412, 'Precondition Failed'),
    (413, 'Request Entity Too Large'),
    (414, 'Request-URI Too Long'),
    (415, 'Unsupported Media Type'),
    (416, 'Requested Range Not Satisfiable'),
    (417, 'Expectation Failed'),
    (418, 'I\'m a teapot'),

    (500, 'Internal Server Error'),
    (501, 'Not Implemented'),
    (502, 'Bad Gateway'),
    (503, 'Service Unavailable'),
    (504, 'Gateway Timeout'),
    (505, 'HTTP Version Not Supported'),
)

STATUS = OrderedDict(STATUS_CODES)
for code, label in STATUS.items():
    setattr(STATUS, re.sub(r'\W', '_', label.upper()), code)


class Response(object):
    default_status_code = STATUS.OK
    def __init__(self, content='', status_code=None, content_type='text/html',
            status_message=None, **kwargs):
        self.content = content
        self.encoding = kwargs.get('encoding', DEFAULT_ENCODING)
        if status_code is None:
            status_code = self.default_status_code
        self.status_code = status_code
        self.status_message = status_message
        self.headers = {}
        self.headers['Content-Type'] = content_type
        self.cookies = SimpleCookie()

    def __iter__(self):
        '''WSGI Iterates response content.'''
        value = self.content
        if not hasattr(value, '__iter__') or isinstance(value, (bytes, str)):
            value = [value]

        for chunk in value:
            # Don't encode when already bytes or Content-Encoding set
            if not isinstance(chunk, bytes):
                chunk = chunk.encode(self.encoding)
            yield chunk

    def build_headers(self):
        '''
        Return the list of headers as two-tuples
        '''
        if not 'Content-Type' in self.headers:
            content_type = self.content_type
            if self.encoding != DEFAULT_ENCODING:
                content_type += '; charset=%s' % self.encoding
            self.headers['Content-Type'] = content_type

        headers = list(self.headers.items())
        # Append cookies
        headers += [
            ('Set-Cookie', cookie.OutputString())
            for cookie in self.cookies.values()
        ]
        return headers

    def add_cookie(self, key, value, **attrs):
        '''
        Finer control over cookies.  Allow specifying an Morsel arguments.
        '''
        if attrs:
            c = Morsel()
            c.set(key, value, **attrs)
            self.cookies[key] = c
        else:
            self.cookies[key] = value

    @property
    def status(self):
        '''Allow custom status messages'''
        message = self.status_message
        if message is None:
            message = STATUS[self.status_code]
        return '%s %s' % (self.status_code, message)

    def close(self):
        '''Close our content if it can be.

        WSGI must call close if the response object has one.
        '''
        if callable(getattr(self.content, 'read', None)):
            self.content.close()


#
# Success Responses (2xx)
#

class ResponseSuccess(Response):
    '''A base class for all 2xx responses, so we can issubclass test.'''

class OK(ResponseSuccess):
    default_status_code = STATUS.OK

class Created(ResponseSuccess):
    default_status_code = STATUS.CREATED

class Accepted(ResponseSuccess):
    default_status_code = STATUS.ACCEPTED

class NoContent(ResponseSuccess):
    default_status_code = STATUS.NO_CONTENT

class ResetContent(ResponseSuccess):
    default_status_code = STATUS.RESET_CONTENT

class PartialContent(ResponseSuccess):
    default_status_code = STATUS.PARTIAL_CONTENT

#
# Redirection Responses (3xx)
#

class ResponseRedirection(Response):
    '''A base class for all 3xx responses.'''

class LocationHeaderMixin(object):
    '''Many 3xx responses require a Location header'''
    allowed_schemes = ('http', 'https')

    def __init__(self, location, *args, **kwargs):
        super(LocationHeaderMixin, self).__init__(*args, **kwargs)
        parsed = urlparse(location)
        if parsed.scheme and parsed.scheme not in self.allowed_schemes:
            raise ValueError(
                "Unsafe redirect to URL with protocol '%s'" % parsed.scheme
            )
        self.headers['Location'] = location # Probably need escaping?

    url = property(lambda self: self.headers['Location'])


class MultipleChoices(ResponseRedirection):
    default_status_code = STATUS.MULTIPLE_CHOICES

class MovedPermanently(LocationHeaderMixin, ResponseRedirection):
    default_status_code = STATUS.MOVED_PERMANENTLY

class Found(LocationHeaderMixin, ResponseRedirection):
    default_status_code = STATUS.FOUND

class SeeOther(LocationHeaderMixin, ResponseRedirection):
    default_status_code = STATUS.SEE_OTHER

class NotModified(ResponseRedirection):
    default_status_code = STATUS.NOT_MODIFIED

class UseProxy(LocationHeaderMixin, ResponseRedirection):
    default_status_code = STATUS.USE_PROXY

class TemporaryRedirect(ResponseRedirection):
    default_status_code = STATUS.TEMPORARY_REDIRECT

class PermanentRedirect(ResponseRedirection):
    default_status_code = STATUS.PERMANENT_REDIRECT

#
# Client Error Responses (4xx)
#

class ResponseError(Response):
    '''A base class for all 4xx responses.'''

class BadRequest(ResponseError):
    default_status_code = STATUS.BAD_REQUEST

# XXX Auth-Realm ?
class Unauthorized(ResponseError):
    default_status_code = STATUS.UNAUTHORIZED

class PaymentRequired(ResponseError):
    default_status_code = STATUS.PAYMENT_REQUIRED

class Forbidden(ResponseError):
    default_status_code = STATUS.FORBIDDEN

class NotFound(ResponseError):
    default_status_code = STATUS.NOT_FOUND

class MethodNotAllowed(ResponseError):
    def __init__(self, permitted_methods, *args, **kwargs):
        super(MethodNotAllowed, self).__init__(*args, **kwargs)
        self.headers['Allow'] = ', '.join(permitted_methods)

    default_status_code = STATUS.METHOD_NOT_ALLOWED

class NotAcceptable(ResponseError):
    default_status_code = STATUS.NOT_ACCEPTABLE

class ProxyAuthenticationRequired(ResponseError):
    default_status_code = STATUS.PROXY_AUTHENTICATION_REQUIRED

class RequestTimeout(ResponseError):
    default_status_code = STATUS.REQUEST_TIMEOUT

class Conflict(ResponseError):
    default_status_code = STATUS.CONFLICT

class Gone(ResponseError):
    default_status_code = STATUS.GONE

class LengthRequired(ResponseError):
    default_status_code = STATUS.LENGTH_REQUIRED

class PreconditionFailed(ResponseError):
    default_status_code = STATUS.PRECONDITION_FAILED

class RequestEntityTooLarge(ResponseError):
    default_status_code = STATUS.REQUEST_ENTITY_TOO_LARGE

class RequestURITooLong(ResponseError):
    default_status_code = STATUS.REQUEST_URI_TOO_LONG

class UnsupportedMediaType(ResponseError):
    default_status_code = STATUS.UNSUPPORTED_MEDIA_TYPE

class RequestedRangeNotSatisfiable(ResponseError):
    default_status_code = STATUS.REQUESTED_RANGE_NOT_SATISFIABLE

class ExpectationFailed(ResponseError):
    default_status_code = STATUS.EXPECTATION_FAILED

#
# Server Error (5xx)
#

class ResponseServerError(Response):
    '''A base class for 5xx responses.'''

class InternalServerError(ResponseServerError):
    default_status_code = STATUS.INTERNAL_SERVER_ERROR

class NotImplemented(ResponseServerError):
    default_status_code = STATUS.NOT_IMPLEMENTED

class BadGateway(ResponseServerError):
    default_status_code = STATUS.BAD_GATEWAY

class ServiceUnavailable(ResponseServerError):
    default_status_code = STATUS.SERVICE_UNAVAILABLE

class GatewayTimeout(ResponseServerError):
    default_status_code = STATUS.GATEWAY_TIMEOUT

class HttpVersiontNotSupported(ResponseServerError):
    default_status_code = STATUS.HTTP_VERSION_NOT_SUPPORTED
