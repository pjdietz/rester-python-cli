import unittest
from unittest import mock
from rester import parse


# -----------------------------------------------------------------------------
# Sample requests

GET = """
GET /my.path HTTP/1.1
Host: my.host.com
"""

POST_PLAIN_TEXT = """
POST /path HTTP/1.1
Content-type: text/plain
X-custom: Custom header
X-custom: Another header

This is the body
"""

NO_PROTOCOL = """
GET /my.path.with.no.protocol
"""

PATH_ONLY = """
/path-only
"""

# -----------------------------------------------------------------------------


class RequestParserTest(unittest.TestCase):

    ###
    # Method
    ###

    def test_parses_method(self):

        factory = mock.Mock()
        parser = parse.RequestParser(factory)

        requests = [
            ("GET", GET),
            ("POST", POST_PLAIN_TEXT),
            ("GET", NO_PROTOCOL),
            ("GET", PATH_ONLY)
        ]

        for method, request in requests:
            parser.parse(request)
            args, kwargs = factory.call_args
            self.assertEqual(kwargs["method"], method)

    ###
    # Headers
    ###

    def test_parses_headers(self):

        factory = mock.Mock()
        parser = parse.RequestParser(factory)
        parser.parse(POST_PLAIN_TEXT)
        args, kwargs = factory.call_args
        self.assertEqual(kwargs["headers"], {
            "Content-type": ["text/plain"],
            "X-custom": ["Custom header", "Another header"]
        })

    ###
    # Body
    ###

    def test_parses_body(self):
        factory = mock.Mock()
        parser = parse.RequestParser(factory)
        parser.parse(POST_PLAIN_TEXT)
        args, kwargs = factory.call_args
        self.assertEqual(kwargs["body"], "This is the body")

    def test_parses_no_body(self):
        factory = mock.Mock()
        parser = parse.RequestParser(factory)
        parser.parse(GET)
        args, kwargs = factory.call_args
        self.assertEqual(kwargs["body"], None)

if __name__ == '__main__':
    unittest.main()