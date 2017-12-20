from importlib import import_module
import json
import os

from django.conf import settings 
from django.core.urlresolvers import Resolver404, resolve
from django.http import Http404
from django.test import RequestFactory
from django.utils.functional import cached_property
import requests


class ApiClient:
    """Retrieve regulations data via Python, HTTP, or disk.

    Optionally define settings.EREGS_REGCORE_URLS to the module name of the
    related cfpb/regulations-core project (e.g. 'regcore.urls') to use a
    runtime import to handle requests instead of HTTP.
    """
    def __init__(self):
        self.base_url = settings.API_BASE

        self.regcore_urls = getattr(settings, 'EREGS_REGCORE_URLS', None)
        if self.regcore_urls:
            self.regcore_urls = import_module(self.regcore_urls)

    def get_from_file_system(self, suffix):
        if os.path.isdir(self.base_url + suffix):
            suffix = suffix + "/index.html"
        f = open(self.base_url + suffix)
        content = f.read()
        f.close()
        return json.loads(content)

    @cached_property
    def request_factory(self):
        return RequestFactory()

    def get_from_http(self, suffix, params={}):
        url = self.base_url + suffix
        r = requests.get(url, params=params)
        if r.status_code == requests.codes.ok:
            return r.json()
        elif r.status_code == 404:
            return None
        else:
            r.raise_for_status()

    def get_from_regcore(self, suffix, params={}):
        path = '/' + suffix

        try:
            func, args, kwargs = resolve(path, urlconf=self.regcore_urls)
        except Resolver404:
            # This mimics the behavior of a 404 from the regcore API for
            # an invalid request that doesn't match a URL pattern.
            return None

        request = self.request_factory.get(path, data=params)

        try:
            response = func(request, *args, **kwargs)
        except Http404:
            return None

        if response.status_code == 404:
            return None

        # This mimics the behavior of requests.raise_for_status:
        # https://github.com/requests/requests/blob/v2.12.4/requests/models.py#L870
        if 400 <= response.status_code < 600:
            raise RuntimeError(
                'regcore path {} returned status code {}: {}'.format(
                    path,
                    response.status_code,
                    response.content
                )
            )

        return json.loads(response.content)

    def get(self, suffix, params={}):
        if self.regcore_urls:
            return self.get_from_regcore(suffix, params=params)
        elif self.base_url.startswith('http'):
            return self.get_from_http(suffix, params=params)
        else:
            return self.get_from_file_system(suffix)
