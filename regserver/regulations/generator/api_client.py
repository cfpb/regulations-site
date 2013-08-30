import json
import os
from django.conf import settings 
import requests


class ApiClient:
    """ Actually go out and make the GET request, or read the disk to acquire
    the required data. """

    def __init__(self):
        self.base_url = settings.API_BASE

    def get_from_file_system(self, suffix):
        if os.path.isdir(self.base_url + suffix):
            suffix = suffix + "/index.html"
        f = open(self.base_url + suffix)
        content = f.read()
        f.close()
        return json.loads(content)

    def get(self, suffix, params={}):
        """Make the GET request. Assume the result is JSON. Right now, there is
        no error handling"""

        if self.base_url.startswith('http'):
            return requests.get(self.base_url + suffix, params=params).json()
        else:
            return self.get_from_file_system(suffix)
