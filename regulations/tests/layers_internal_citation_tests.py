from regulations.generator.layers.internal_citation import InternalCitationLayer
from mock import patch
from unittest import TestCase

class InternalCitationLayerTest(TestCase):

    @patch('regulations.generator.layers.internal_citation.loader')
    def test_render_url(self, loader):
        icl = InternalCitationLayer(None)

        icl.render_url(['888', '123'], 'link')
        context = loader.get_template.return_value.render.call_args[0][0]
        self.assertEqual('#888-123', context['citation']['url'])
        self.assertEqual('link', context['citation']['label'])

        icl.sectional = True
        icl.version = 'vvvv'
        icl.render_url(['888', '123'], 'look')
        context = loader.get_template.return_value.render.call_args[0][0]

        self.assertTrue('888-123/vvvv#888-123' in context['citation']['url'])
        self.assertEqual('look', context['citation']['label'])
