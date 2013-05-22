import re
from unittest import TestCase
from layers import layers_applier

class SearchReplaceLayersTest(TestCase):
    def test_replace_at_offset(self):
        srl = layers_applier.SearchReplaceLayersApplier()

        text = 'The cat sat on a hat'
        offsets = srl.find_all_offsets('cat', text)
        offset = offsets[0]

        modified_text = srl.replace_at_offset(offset, text, 'monkey')
        self.assertEquals(modified_text, 'The monkey sat on a hat')

    def test_find_all_offsets(self):
        srl = layers_applier.SearchReplaceLayersApplier()

        text = "Find all the offsets, all of them"
        offsets = srl.find_all_offsets('all', text)
        self.assertEqual(offsets, [(5,8), (22, 25)])
        self.assertEqual(len(offsets), 2)

