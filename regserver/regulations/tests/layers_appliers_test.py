from unittest import TestCase
from regulations.generator.layers import layers_applier
from regulations.generator.layers import location_replace

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
        offsets = location_replace.LocationReplace.find_all_offsets(pattern, text)
        self.assertEquals(offsets, [(13, 17), (40, 44)])

    def test_find_offsets_no_pattern(self):
        pattern = 'ABCD'
        text = 'The grey fox jumped over the fence'
        offsets = location_replace.LocationReplace.find_all_offsets(pattern, text)
        self.assertEquals(offsets, [])

    def test_replace_at_offset(self):
        pattern = 'ABCD'
        text = 'The grey fox ABCD jumped over the fence ABCD'

        first_offset = location_replace.LocationReplace.find_all_offsets(pattern, text)[0]
        result = location_replace.LocationReplace.replace_at_offset(first_offset, 'giraffe', text)

        self.assertEquals(result, 'The grey fox giraffe jumped over the fence ABCD')

    def test_replace_at(self):
        text = 'The grey fox ABCD jumped ABCD over the fence ABCD'

        applier = layers_applier.LayersApplier()
        applier.text = text
        applier.replace_at('ABCD', '<a>ABCD</a>', [0,2])

        self.assertEquals(applier.text, 'The grey fox <a>ABCD</a> jumped ABCD over the fence <a>ABCD</a>')

    def test_update_offsets(self):
        lr = location_replace.LocationReplace()
        lr.offset_starter = 5

        pattern = 'ABCD'
        text = 'The grey <a href="link">ABCD</a> jumped over the ABCD fence on a ABCD day'

        lr.update_offsets(pattern, text)
        self.assertEquals(lr.counter, 0)
        self.assertEqual(lr.offset_starter, 5)
        self.assertEqual(lr.offset_counters, [5,6,7])
        self.assertEqual(lr.offsets.keys(), [5, 6, 7])
        self.assertEqual(lr.offsets[5], (24,28))

    def test_update_offset_starter(self):
        lr = location_replace.LocationReplace()
        lr.offset_counters = [5,6,7]
        lr.update_offset_starter()

        self.assertEqual(lr.offset_starter, 8)

    def test_replace_at_case_sensitive(self):
        original =  'state'
        replacement = '<a href="link_url">state</a>'
        locations = [0, 1, 2]

        applier = layers_applier.LayersApplier()
        applier.text = "<em>(6)</em> <dfn> Under state law. </dfn> State law."
        applier.replace_at(original, replacement, locations)

        result = u"<em>(6)</em> <dfn> Under <a href=\"link_url\">state</a> law. </dfn> State law."
        self.assertEquals(applier.text, result)

    def test_replace_no_original(self):
        original =  'federal'
        replacement = '<a href="link_url">state</a>'
        locations = [0, 1, 2]

        applier = layers_applier.LayersApplier()
        applier.text = "<em>(6)</em> <dfn> Under state law. </dfn> State law."
        applier.replace_at(original, replacement, locations)

        result = "<em>(6)</em> <dfn> Under state law. </dfn> State law."
        self.assertEquals(applier.text, result)

    def test_replace_skip_location(self):
        original =  'state'
        replacement = '<a href="link_url">state</a>'
        locations = [0, 2]

        applier = layers_applier.LayersApplier()
        applier.text = "<em>(6)</em> <dfn> Under state law. </dfn> state law. <dfn> state liability. </dfn>"
        applier.replace_at(original, replacement, locations)

        result = "<em>(6)</em> <dfn> Under <a href=\"link_url\">state</a> law. </dfn> state law. <dfn> <a href=\"link_url\">state</a> liability. </dfn>"
        self.assertEquals(applier.text, result)

