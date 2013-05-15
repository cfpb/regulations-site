import json
from urllib import urlopen

class Client:
    """A very simple client for accessing the regulation and meta data."""

    def __init__(self, base_url):
        self.base_url = base_url

    def regulation(self, label, version):
        """End point for regulation JSON. Return the result as a dict"""
        return self._get("regulation/%s/%s" % (label, version))

    def layer(self, layer_name, label, version):
        """End point for layer JSON. Return the result as a list"""
        return self._get("layer/%s/%s/%s" % (layer_name, label, version))

    def notices(self):
        """End point for notice searching. Right now, just a list"""
        return self._get("notice")

    def notice(self, document_number):
        """End point for retrieving a single notice."""
        return self._get("notice/%s" % document_number)

    def _get(self, suffix):
        """Actually make the GET request. Assume the result is JSON. Right
        now, there is no error handling"""
        try:
            result = urlopen(self.base_url + suffix)
        except IOError: #   Hack to deal with local FS vs API
            result = urlopen(self.base_url + suffix + "/index.html")
        content = result.read()
        result.close()
        return json.loads(content)
