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
        self.assertEqual('#I-2322-3-z9xii-1', context['citation']['url'])

    def test_create_sectional_url_parts(self):
        u = InternalCitationLayer.create_sectional_url_parts({
                'citation': ['2322',  '3', 'a', '1'],
        })
        self.assertEqual(('2322-3', '#2322-3-a-1'), u)

    @patch('regulations.generator.layers.internal_citation.loader')
    def test_render_url(self, loader):
        InternalCitationLayer.render_url('/abcd/123', 'link', 'template.html')
        context = loader.get_template.return_value.render.call_args[0][0]
        self.assertEqual('/abcd/123', context['citation']['url'])
        self.assertEqual('link', context['citation']['label'])
