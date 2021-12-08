from bottle import Bottle, request


class BasicAuth:
    def __init__(self, path="/"):
        pass

    def setup(self, app: Bottle):
        # Register endpoints
        pass

    def apply(self, callback, context):
        headers = request.headers
        auth_header = headers.get("Authorization")
        parts = auth_header.split()
