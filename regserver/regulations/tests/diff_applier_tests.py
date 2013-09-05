from unittest import TestCase
from regulations.generator.layers import diff_applier

from collections import deque


class DiffApplierTest(TestCase):

    def test_create_applier(self):
        diff = {'some': 'diff'}
        da = diff_applier.DiffApplier(diff)
        self.assertEquals(da.diff, diff)

    def create_diff_applier(self):
        diff = {'some': 'diff'}
        da = diff_applier.DiffApplier(diff)
        text = "abcd"
        da.deconstruct_text(text)
        return da

    def test_deconstruct_text(self):
        da = self.create_diff_applier()

        self.assertTrue('oq' in da.__dict__)

        deque_list = [
            deque(['a']), deque(['b']),
            deque(['c']), deque(['d'])]

        self.assertEquals(da.oq, deque_list)

    def test_insert_text(self):
        da = self.create_diff_applier()

        da.insert_text(1, 'AA')
        deque_list = [
            deque(['a']), deque(['b', '<ins>', 'AA', '</ins>']),
            deque(['c']), deque(['d'])]
        self.assertEquals(da.oq, deque_list)

    def test_insert_text_at_end(self):
        da = self.create_diff_applier()

        da.insert_text(4, 'AA')
        deque_list = [
            deque(['a']), deque(['b']),
            deque(['c']), deque(['d', '<ins>', 'AA', '</ins>'])]
        self.assertEquals(da.oq, deque_list)

    def test_delete_text(self):
        da = self.create_diff_applier()
        da.delete_text(0, 2)
        deque_list = [
            deque(['<del>', 'a']), deque(['b', '</del>']),
            deque(['c']), deque(['d'])]
        self.assertEquals(da.oq, deque_list)

    def test_apply_diff(self):
        diff = {'204': {'text': [('delete', 0, 2), ('insert', 4, 'AAB')], 'op':''}}
        da = diff_applier.DiffApplier(diff)
        da.apply_diff('acbd', '204')

        new_text = da.get_text()
        self.assertEquals('<del>ac</del>bd<ins>AAB </ins>', new_text)

    def test_delete_all(self):
        da = diff_applier.DiffApplier({})
        original = 'abcd'
        deleted = da.delete_all(original)
        self.assertEqual('<del>abcd</del>', deleted)
