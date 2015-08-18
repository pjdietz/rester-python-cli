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

HTTP_1_0 = """GET /old-stuff HTTP/1.0"""

NO_PROTOCOL = """
GET /my.path.with.no.protocol
"""

HOST_AND_PATH = """GET host.com/path"""

SCHEME_HOST_AND_PATH = """GET http://scheme.host.com/path"""

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
            (GET, "GET"),
            (POST_PLAIN_TEXT, "POST"),
            (NO_PROTOCOL, "GET"),
            (PATH_ONLY, "GET")
        ]

        for request, method in requests:
            parser.parse(request)
            args, kwargs = factory.call_args
            self.assertEqual(kwargs["method"], method)

    ###
    # Path
    ###

    def test_parses_path(self):

        factory = mock.Mock()
        parser = parse.RequestParser(factory)

        requests = [
            (GET, "/my.path"),
            (POST_PLAIN_TEXT, "/path"),
            (NO_PROTOCOL, "/my.path.with.no.protocol"),
            (PATH_ONLY, "/path-only"),
            (HOST_AND_PATH, "/path"),
            (SCHEME_HOST_AND_PATH, "/path")
        ]

        for request, path in requests:
            parser.parse(request)
            args, kwargs = factory.call_args
            self.assertEqual(kwargs["path"], path)

    ###
    # Protocol version
    ###

    def test_parses_protocol_version(self):

        factory = mock.Mock()
        parser = parse.RequestParser(factory)

        requests = [
            (GET, "1.1"),
            (POST_PLAIN_TEXT, "1.1"),
            (NO_PROTOCOL, "1.1"),
            (PATH_ONLY, "1.1"),
            (HOST_AND_PATH, "1.1"),
            (SCHEME_HOST_AND_PATH, "1.1"),
            (HTTP_1_0, "1.0")
        ]

        for request, protocol_version in requests:
            parser.parse(request)
            args, kwargs = factory.call_args
            self.assertEqual(kwargs["protocol_version"], protocol_version)

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
