from urllib.parse import urlparse


class RequestParser():
    """Creates a new Request object given a string request"""

    def __init__(self, request_factory):
        self.request_factory = request_factory

    def parse(self, request):
        """Return a Request object and a dict of configuration options"""

        # Dictionary of configuration extracted from the request string.
        config = {}

        request = request.strip()

        # Split the request into head and body
        if "\n\n" in request:
            head, body = request.split("\n\n", 1)
        else:
            head = request
            body = None

        headers = head.split("\n")
        request_line = headers[0]
        headers = headers[1:]
        headers = self.parse_headers(headers)

        # The first line of the head is the request line.
        method, path, protocol = self.parse_request_line(request_line)

        # Ensure the path include only a path.
        url = urlparse(path)
        path = url[2]
        if path[0] != "/":
            url = urlparse("//" + path)
            path = url[2]

        rqst = self.request_factory(
            method=method,
            path=path,
            protocol=protocol,
            headers=headers,
            body=body)

        return rqst, config

    @staticmethod
    def parse_request_line(line):
        """Return a tuple of method, path, protocol"""

        spaces = line.count(" ")
        # Entire line is the path
        if spaces == 0:
            return "GET", line, "HTTP/1.1"
        # Assume Method Path Protocol
        elif spaces == 2:
            return line.split(" ")
        # Treat as Method Path. Any other text is discarded.
        else:
            method, path = line.split(" ")
            return method, path, "HTTP/1.1"

    @staticmethod
    def parse_headers(lines):
        """Return a dict of headers given header lines"""
        headers = {}
        for line in lines:
            name, value = line.split(":")
            name = name.strip()
            value = value.strip()
            if not name in headers:
                headers[name] = []
            headers[name].append(value)
        return headers
