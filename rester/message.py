class Message(object):
    """Base class for HTTP messages"""

    def __init__(self, headers=None, body=None):

        if headers is None:
            headers = []

        self.headers = headers
        self.body = body


class Request(Message):
    """Represents an HTTP request"""

    def __init__(self, headers=None, body=None):
        Message.__init__(self, headers=headers, body=body)

