
'''
Classes to parse RFC 2388 mime/multipart content
'''
from collections import defaultdict

class MultipartParser(
    def __init__(self, content, boundary):
        self.boundary = ('--' + boundary).encode('ascii')
        self.terminator = ('--' + boundary + '--').encode('ascii')
        self.lines = iter(content.splitlines())

    def parse(self):
        data = defaultdict(list)
        for part in self.parse_part():
            if part.disposition != b'form-data':
                raise ValueError('Invalid content type: %r' % part.content_type)
            data[part.opts['name']] = part.content
        return data

    def parse_part(self):
        line = self.lines.next()
        # Scan to next boundary
        while line != self.boundary:
            line = self.lines.next()

        p = Part()
        # Parse headers
        while line:
            name, _, data = line.partition(b':')
            name = name.lower()
            if name == b'content-disposition':
                bits = name.split(b';')
                p.content_type = bits.pop(0)
                for param in bits:
                    k, _, v = param.strip().partition(b'=')
                    p.opts[k] = v
                p.name = opts[b'name']
            elif name == b'content-type':
                p.content_type = data.strip()

        data = []
        line = line.next()
        p.data = b''.join(
            line for line in self.lines

class Part(object):
    '''
    Encapsulates a MIME part
    '''
    def __init__(self):
        self.content_type = None
        self.disposition = None
        self.name = None
        self.opts = {}
        self.content = None
        self.headers = {}
