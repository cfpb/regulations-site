import copy
import json
import os

import requests


class Client:
    """A very simple client for accessing the regulation and meta data."""
    _reg_cache = {}
    _layer_cache = {}

    def _dfs_search(self, reg_tree, index):
        """Find the matching node in the tree (if it exists)"""
        if '-'.join(reg_tree['label']) == index:
            return reg_tree
        for child in reg_tree['children']:
            child_search = self._dfs_search(child, index)
            if child_search:
                return child_search

    def _use_reg_cache(self, label, version):
        """See if we've already grabbed that id. Cache results if not.
        @todo: add a timeout"""
        if (label, version) in Client._reg_cache:
            return Client._reg_cache[(label, version)]
        for cache_label, cache_version in Client._reg_cache:
            if cache_version == version and label.startswith(cache_label):
                matching_child = self._dfs_search(
                    Client._reg_cache[(cache_label, cache_version)], label)
                if matching_child:
                    Client._reg_cache[(label, version)] = matching_child
                    return matching_child
        Client._reg_cache[(label, version)] = self._get(
            "regulation/%s/%s" % (label, version))
        return Client._reg_cache[(label, version)]

    def __init__(self, base_url):
        self.base_url = base_url

    def regulation(self, label, version):
        """End point for regulation JSON. Return the result as a dict"""
        return copy.deepcopy(self._use_reg_cache(label, version))
        #return self._get("regulation/%s/%s" % (label, version))

    def diff(self, label, older, newer):
        """ End point for diff JSON. """
        return self._get("diff/%s/%s/%s" % (label, older, newer))

    def regversions(self, label):
        """End point for getting a list of regulation versions."""
        return self._get("regulation/%s" % label)

    def layer(self, layer_name, label, version):
        """Check the layer cache to see if we've already requested this
        version+layer. We just grab once for the entire regulation."""
        ident = (layer_name, label.split('-')[0], version)
        if ident not in Client._layer_cache:
            Client._layer_cache[ident] = self._get("layer/%s/%s/%s" % ident)
        return Client._layer_cache[ident]

    def notices(self, part=None):
        """End point for notice searching. Right now, just a list"""
        if part:
            return self._get("notice", {'part': part})
        else:
            return self._get("notice")

    def notice(self, document_number):
        """End point for retrieving a single notice."""
        return self._get("notice/%s" % document_number)

    def _get(self, suffix, params=None):
        """Actually make the GET request. Assume the result is JSON. Right
        now, there is no error handling"""
        if not params:
            params = {}
        print self.base_url + suffix
        if self.base_url.startswith('http'):    # API
            return requests.get(self.base_url + suffix, params=params).json()
        else:   # file system
            if os.path.isdir(self.base_url + suffix):
                suffix = suffix + "/index.html"
            f = open(self.base_url + suffix)
            content = f.read()
            f.close()
            return json.loads(content)
