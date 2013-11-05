from unittest import TestCase
from regulations.generator.layers import diff_applier
from regulations.generator.layers import tree_builder
from regulations.generator.node_types import REGTEXT

from collections import deque


class DiffApplierTest(TestCase):

    def test_create_applier(self):
        diff = {'some': 'diff'}
        da = diff_applier.DiffApplier(diff, None)
        self.assertEquals(da.diff, diff)

    def create_diff_applier(self):
        diff = {'some': 'diff'}
        da = diff_applier.DiffApplier(diff, None)
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
            deque(['a']), deque(['<ins>AA</ins>', 'b']),
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
        diff = {'204': {'text': [('delete', 0, 2), ('insert', 4, 'AAB')],
                        'op': ''}}
        da = diff_applier.DiffApplier(diff, None)
        da.apply_diff('acbd', '204')
        new_text = da.get_text()
        self.assertEquals('<del>ac</del>bd<ins>AAB</ins>', new_text)

    def test_apply_diff_title(self):
        diff = {'204': {'title': [('delete', 0, 2), ('insert', 4, 'AAC')],
                        'text':  [('delete', 0, 2), ('insert', 4, 'AAB')],
                        'op': ''}}
        da = diff_applier.DiffApplier(diff, None)
        da.apply_diff('acbd', '204', component='title')
        new_text = da.get_text()
        self.assertEquals('<del>ac</del>bd<ins>AAC</ins>', new_text)

    def test_delete_all(self):
        da = diff_applier.DiffApplier({}, None)
        original = 'abcd'
        deleted = da.delete_all(original)
        self.assertEqual('<del>abcd</del>', deleted)

    def build_tree(self):
        child = {
            'text': 'child text',
            'children': [],
            'label_id': '204-3',
            'label': ['204', '3'],
            'node_type': REGTEXT
        }
        tree = {
            'text': 'parent text',
            'children': [child],
            'label_id': '204',
            'label': ['204'],
            'node_type': REGTEXT
        }
        return tree

    def test_add_nodes_to_tree(self):
        tree = self.build_tree()

        new_node = {
            'text': 'child text',
            'children': [],
            'label_id': '204-2',
            'label': ['204', '2'],
            'node_type': REGTEXT
        }

        da = diff_applier.DiffApplier({}, None)
        adds = tree_builder.AddQueue()
        adds.insert_all([('204-2', new_node)])

        da.add_nodes_to_tree(tree, adds)
        self.assertEqual(len(tree['children']), 2)
        self.assertEqual(tree['children'][0], new_node)

    def test_add_nodes_new_section(self):
        tree = self.build_tree()
        new_node = {
            'text': 'new node text',
            'children': [],
            'label_id': '204-2',
            'label': ['204', '2'],
            'node_type': REGTEXT
        }
        new_node_child = {
            'text': 'new node child text',
            'children': [],
            'label_id': '204-2-a',
            'label': ['204', '2', 'a'],
            'node_type': REGTEXT
        }
        da = diff_applier.DiffApplier({}, None)
        adds = tree_builder.AddQueue()
        adds.insert_all([('204-2-a', new_node_child), ('204-2', new_node)])
        da.add_nodes_to_tree(tree, adds)
        self.assertEqual(len(tree['children']), 2)

        new_node['children'].append(new_node_child)
        self.assertEqual(tree['children'][0], new_node)

    def test_add_nodes_empty_tree(self):
        tree = {}
        new_node = {
            'text': 'new node text',
            'children': [],
            'label_id': '204-2',
            'label': ['204', '2'],
            'node_type': REGTEXT
        }
        da = diff_applier.DiffApplier({}, None)
        adds = tree_builder.AddQueue()
        adds.insert_all([('204-2', new_node)])

        da.add_nodes_to_tree(tree, adds)

    def test_child_picking(self):
        da = self.create_diff_applier()
        da.label_requested = '204-3'

        self.assertTrue(da.is_child_of_requested('204-3-a'))
        self.assertFalse(da.is_child_of_requested('204-32'))

        da.label_requested = '204-3-Interp'
        self.assertTrue(da.is_child_of_requested('204-3-a-Interp'))
        self.assertTrue(da.is_child_of_requested('204-3-Interp-1'))
        self.assertFalse(da.is_child_of_requested('204-30-Interp'))

        da.label_requested = '204-3-Interp-4'
        self.assertFalse(da.is_child_of_requested('204-3-a-Interp'))
        self.assertFalse(da.is_child_of_requested('204-3-Interp-1'))
        self.assertTrue(da.is_child_of_requested('204-3-Interp-4-a'))

    def test_tree_changes_new_section(self):
        diff = {'9999-25': {'op': 'added',
                            'node': {'text': 'Some Text',
                                     'node_type': 'REGTEXT',
                                     'label': ['9999', '25'],
                                     'children': []}}}
        old_tree = {}
        da = diff_applier.DiffApplier(diff, '9999-25')
        da.tree_changes(old_tree)

        self.assertEqual(old_tree['label'], ['9999', '25'])
