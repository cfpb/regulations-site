from regulations.generator.layers.definitions import DefinitionsLayer
from mock import patch
from unittest import TestCase

class DefinitionsLayerTest(TestCase):
    @patch('regulations.generator.layers.internal_citation.loader')
    def test_create_definition_link(self, loader):
        rt = DefinitionsLayer.create_definition_link('abc', ['202', '3'])
        context = loader.get_template.return_value.render.call_args[0][0]
        self.assertEquals('#202-3', context['citation']['url'])

    @patch('regulations.generator.layers.internal_citation.loader')
    def test_create_layer_pair(self, loader):
        layer = {
            '202-3':{'ref':'account:202-2-a'},
            'referenced':{'account:202-2-a': {'reference':'202-2-a'}}
        }

        dl = DefinitionsLayer(layer)
        layer_pair = dl.create_layer_pair('I have an account', (10, 16), layer['202-3'])
        context = loader.get_template.return_value.render.call_args[0][0]
        self.assertEquals('#202-2-a', context['citation']['url'])
