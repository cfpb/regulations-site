from regulations.generator.layers.definitions import DefinitionsLayer
from unittest import TestCase

class DefinitionsLayerTest(TestCase):
    def test_create_url(self):
        url = DefinitionsLayer.create_url(['303', '1'])
        self.assertEquals('#303-1', url)

    def test_create_url_single(self):
        url = DefinitionsLayer.create_url(['303'])
        self.assertEquals('#303', url)

    def test_create_definition_reference(self):
        ref = DefinitionsLayer.create_definition_reference(['303', '1'])
        self.assertEquals('303-1', ref)

    def test_create_definition_link(self):
        layer = {
            '202-3':{'ref':'account:202-2-a'},
            'referenced':{'account:202-2-a': {'reference':'202-2-a'}}
            }
        dl = DefinitionsLayer(layer)
        definition_link = dl.create_definition_link('account', ['202', '3'])

        url = '<a href="#202-3" class="citation definition" data-definition="202-3">account</a>'
        self.assertEquals(definition_link, url)
