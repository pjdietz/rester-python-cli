class RequestParser():
    """Creates a new Request object given a string request"""

    def __init__(self, request_factory):
        self.request_factory = request_factory

    def parse(self, request):

        request = request.strip()

        # Split the request into head and body
        if "\n\n" in request:
            head, body = request.split("\n\n", 1)
        else:
            head = request
            body = None

        return self.request_factory(body=body)


