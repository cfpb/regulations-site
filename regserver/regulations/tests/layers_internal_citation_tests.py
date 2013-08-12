from regulations.generator.layers.internal_citation import InternalCitationLayer
from mock import patch
from unittest import TestCase

class InternalCitationLayerTest(TestCase):

    def test_url_for(self):
        self.assertEqual('/regulation/999-88/verver#999-88-e',
            InternalCitationLayer.sectional_url_for(['999', '88', 'e'],
            'verver'))
        self.assertEqual('/regulation/999-88-Interp/verver#999-88-e-Interp-1',
            InternalCitationLayer.sectional_url_for(['999', '88', 'e',
            'Interp', '1'], 'verver'))
        self.assertEqual('/regulation/999-Interp/verver#999-Interp',
            InternalCitationLayer.sectional_url_for(['999', 'Interp'],
            'verver'))
        self.assertEqual('#999-88-e',
            InternalCitationLayer.hash_url_for(['999', '88', 'e'], 'verver'))

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
        self.assertEqual('/regulation/888-123/vvvv#888-123', 
                context['citation']['url'])
        self.assertEqual('look', context['citation']['label'])
