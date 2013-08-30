import tempfile
import os
import shutil

from regulations.generator.api_client import ApiClient
from unittest import TestCase


class ClientTest(TestCase):
    def test_local_filesystem(self):
        """ Verify that it's possible to host the files locally, where
        index.html is used in place of just the directory name. """
        tmp_root = tempfile.mkdtemp() + os.sep
        notice_path = tmp_root + os.sep + "notice" + os.sep
        os.mkdir(notice_path)
        with open(notice_path + "index.html", 'w') as f:
            f.write('{"results": ["example"]}')
        client = ApiClient()
        client.base_url = tmp_root
        results = client.get('notice')
        shutil.rmtree(tmp_root)
        self.assertEqual(["example"], results['results'])
