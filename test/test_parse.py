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

This is the body
"""

# -----------------------------------------------------------------------------


class RequestParserTest(unittest.TestCase):

    ###
    # Body
    ###

    def test_parses_body(self):
        factory = mock.Mock()
        parser = parse.RequestParser(factory)
        parser.parse(POST_PLAIN_TEXT)
        factory.assert_called_with(body="This is the body")

    def test_parses_no_body(self):
        factory = mock.Mock()
        parser = parse.RequestParser(factory)
        parser.parse(GET)
        factory.assert_called_with(body=None)

if __name__ == '__main__':
    unittest.main()