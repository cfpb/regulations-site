from unittest import TestCase
from regulations.generator.layers import tree_builder
from regulations.generator.node_types import REGTEXT

class TreeBuilderTest(TestCase):

    def build_tree(self):
        child = {
            'text': 'child text',
            'children': [],
            'label_id': '204-3',
            'label': ['204','3'],
            'node_type': REGTEXT
        }
        tree = {
            'text':'parent text', 
            'children': [child],
            'label_id': '204',
            'label': ['204'],
            'node_type': REGTEXT
        }
        return tree

    def test_parent_in_tree(self):
    
        tree = self.build_tree()
        tree_hash = tree_builder.build_tree_hash(tree)
        self.assertEqual(tree_hash.keys(), ['204-3', '204'])

        candidate = '204-3-a'
        parent_label = tree_builder.parent_label(candidate)
        self.assertTrue(tree_builder.parent_in_tree(parent_label, tree_hash))

    def test_add_node(self):
        new_node = {
            'text': 'new node text',
            'children': [],
            'label_id': '204-4',
            'label': ['204','4'],
            'node_type': REGTEXT
        }
        tree = self.build_tree()
        tree_hash = tree_builder.build_tree_hash(tree)
        self.assertEqual(tree_hash.keys(), ['204-3', '204'])

        self.assertEqual(len(tree_hash['204']['children']), 1)
        tree_builder.add_node_to_tree(new_node, '204', tree_hash)
        self.assertEqual(len(tree_hash['204']['children']), 2)
        
        child_labels = [c['label_id'] for c in tree_hash['204']['children']]
        self.assertEqual(child_labels, ['204-3', '204-4'])

    def test_make_label_sortable_roman(self):
        label = "iv"
        sortable = tree_builder.make_label_sortable(label, roman=True)
        self.assertEquals(sortable, 4)

    def test_make_label_sortable_not_roman(self):
        label = "iv"
        sortable = tree_builder.make_label_sortable(label)
        self.assertEquals(sortable, label)
