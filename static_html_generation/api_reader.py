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

    def _get(self, suffix):
        """Actually make the GET request. Assume the result is JSON. Right
        now, there is no error handling"""
        result = urlopen(self.base_url + suffix)
        content = result.read()
        result.close()
        return json.loads(content)
