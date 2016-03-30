from unittest import TestCase

from regulations.generator.layers.definitions import DefinitionsLayer


class DefinitionsLayerTest(TestCase):
    def test_create_definition_link(self):
        layer = {
            '202-3': {'ref': 'account:202-2-a'},
            'referenced': {'account:202-2-a': {'reference': '202-2-a'}}
            }
        dl = DefinitionsLayer(layer)
        definition_link = dl.create_definition_link('account',
                                            ['202', '3'], 'account')

        url = '<a href="#202-3" class="citation definition" '
        url += 'data-definition="202-3" data-defined-term="account" data-gtm_ignore="true">'
        url += 'account</a>'
        self.assertEquals(definition_link, url)
