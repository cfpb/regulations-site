from regulations.generator.layers.internal_citation import InternalCitationLayer
from mock import patch
from unittest import TestCase

class InternalCitationLayerTest(TestCase):
    @patch('regulations.generator.layers.internal_citation.loader')
    def test_create_link_interp(self, loader):
        InternalCitationLayer.create_link("", {
            'citation': ['2322', 'Interpretations', '3', '(z)(9)(xii)', '1'],
        })
        context = loader.get_template.return_value.render.call_args[0][0]
        self.assertEqual('I-2322-3-z9xii-1', context['citation']['url'])
