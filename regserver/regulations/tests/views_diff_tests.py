from unittest import TestCase

from mock import patch
from django.test.client import Client

class PartialSectionDiffViewTest(TestCase):
    @patch('regulations.generator.generator')
    def test_get_404(self, generator):
        generator.get_tree_paragraph.return_value = None
        response = Client().get('/partial/diff/111/222')
        self.assertEqual(404, response.status_code)
