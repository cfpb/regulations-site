import re
from unittest import TestCase
from layers import layers_applier

class LayersApplierTest(TestCase):

    def test_enqueue(self):
        applier = layers_applier.LayersApplier()
        element = ('abcd', 'ABCD', [])
        applier.enqueue(element)

        priority, retrieved = applier.queue.get()
        self.assertEquals(priority, -4)
        self.assertEquals(retrieved, element)

    def test_list_enqueue(self):
        applier = layers_applier.LayersApplier()
        elements = [('abcd', 'ABCD', []), ('efghi', 'EFG', [12])]
        applier.enqueue_from_list(elements)

        priority, retrieved = applier.queue.get()
        self.assertEquals(priority, -5)
        self.assertEqual(elements[1], retrieved)

        priority, retrieved = applier.queue.get()
        self.assertEquals(priority, -4)
        self.assertEqual(elements[0], retrieved)

    def test_replace_all(self):
        applier = layers_applier.LayersApplier()
        applier.text = 'Prefix test <a href="url" data="test">link test</a> postfix text'
        applier.replace_all('test', 'linksecondword')

        replaced = 'Prefix linksecondword <a href="url" data="test">link linksecondword</a> postfix text'
        self.assertEquals(applier.text, replaced)

    def test_find_all_offsets(self):
        pattern = 'ABCD'
        text = 'The grey fox ABCD jumped over the fence ABCD'
        offsets = layers_applier.LayersApplier.find_all_offsets(pattern, text)
        self.assertEquals(offsets, [(13, 17), (40, 44)])

    def test_find_offsets_no_pattern(self):
        pattern = 'ABCD'
        text = 'The grey fox jumped over the fence'
        offsets = layers_applier.LayersApplier.find_all_offsets(pattern, text)
        self.assertEquals(offsets, [])

    def test_replace_at_offset(self):
        pattern = 'ABCD'
        text = 'The grey fox ABCD jumped over the fence ABCD'

        first_offset = layers_applier.LayersApplier.find_all_offsets(pattern, text)[0]
        result = layers_applier.LayersApplier.replace_at_offset(first_offset, 'giraffe', text)

        self.assertEquals(result, 'The grey fox giraffe jumped over the fence ABCD')

    def test_replace_at(self):
        pattern = 'ABCD'
        text = 'The grey fox ABCD jumped ABCD over the fence ABCD'

        applier = layers_applier.LayersApplier()
        applier.text = text
        applier.replace_at('ABCD', '<a>ABCD</a>', [0,2])

        self.assertEquals(applier.text, 'The grey fox <a>ABCD</a> jumped ABCD over the fence <a>ABCD</a>')
