from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser


class ObjectJSONParser(JSONParser):
    """All application write contracts expect an object, not an array/scalar."""

    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(stream, media_type, parser_context)
        if not isinstance(data, dict):
            raise ParseError("Expected a JSON object.")
        return data
