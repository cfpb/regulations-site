from unittest import TestCase

from regulations.generator.layers.definitions import DefinitionsLayer


class DefinitionsLayerTest(TestCase):
    def test_create_url(self):
        dl = DefinitionsLayer(None)
        url = dl.create_url(['303', '1'])
        self.assertEquals('#303-1', url)

        url = dl.create_url(['303', '1', 'b'])
        self.assertEquals('#303-1-b', url)

        url = dl.create_url(['303'])
        self.assertEquals('#303', url)

        dl.sectional = True
        dl.version = 'vvv'
        url = dl.create_url(['303', '1', 'b'])
        self.assertEquals('/303-1/vvv#303-1-b', url)

    def test_create_definition_reference(self):
        ref = DefinitionsLayer.create_definition_reference(['303', '1'])
        self.assertEquals('303-1', ref)

    def test_create_definition_link(self):
        layer = {
            '202-3': {'ref': 'account:202-2-a'},
            'referenced': {'account:202-2-a': {'reference': '202-2-a'}}
            }
        dl = DefinitionsLayer(layer)
        definition_link = dl.create_definition_link('account', ['202', '3'])

        url = '<a href="#202-3" class="citation definition" '
        url += 'data-definition="202-3">account</a>'
        self.assertEquals(definition_link, url)
