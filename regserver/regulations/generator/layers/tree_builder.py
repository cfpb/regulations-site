import re
import itertools

class AddQueue(object):
    """ Maintain a sorted list of nodes to add. This maintains a sorted queue of 
    (label, node) tuples. """

    def __init__(self):
        self.queue = []

    def sort(self):
        self.queue = sorted(self.queue, key=lambda x: len(x[0]), reverse=True)

    def insert(self, item):
        self.queue.append(item)
        self.sort()
    
    def insert_all(self, items):
        self.queue += items
        self.sort()

    def find(self, label):
        found_nodes = [n for n in self.queue if n[0]==label]
        if found_nodes:
            return found_nodes[0]

    def delete(self, label):
        node_removed = [n for n in self.queue if n[0] != label]
        self.queue = node_removed


def build_label(node):
    return '-'.join(node['label'])

def build_tree_hash(tree):
    """ Build a hash map of a tree's nodes, so that we don't 
    have to keep walking the tree. """
    tree_hash = {}

    if tree:
        label_id = build_label(tree)
        tree_hash[label_id] = tree

        for c in tree['children']:
            label_id = build_label(c)
            tree_hash[label_id] = c
    return tree_hash

def parent_label(node_label):
    parent_label = node_label.rsplit("-", 1)[0]
    return parent_label

def parent_in_tree(parent_label, tree_hash):
    """ Return True if the parent of node_label is in the tree """
    return parent_label in tree_hash

def add_node_to_tree(node, parent_label, tree_hash):
    """ Add the node to the tree by adding it to it's parent in order. """
    parent_node = tree_hash[parent_label]
    add_child(parent_node, node)
    return tree_hash

def roman_nums():
    """Generator for roman numerals."""
    mapping = [
        (1, 'i'), (4, 'iv'), (5, 'v'), (9, 'ix'),
        (10, 'x'), (40, 'xl'), (50, 'l'), (90, 'xc'),
        (100, 'c'), (400, 'cd'), (500, 'd'), (900, 'cm'),
        (1000, 'm')
        ]
    i = 1
    while True:
        next_str = ''
        remaining_int = i
        remaining_mapping = list(mapping)
        while remaining_mapping:
            (amount, chars) = remaining_mapping.pop()
            while remaining_int >= amount:
                next_str += chars
                remaining_int -= amount
        yield next_str
        i += 1

def make_label_sortable(label, roman=False):
    """ Appendices have labels that look like 30(a), we make those
    appropriately sortable. """

    if label.isdigit():
        return int(label)
    if label.isalpha():
        if roman:
            #If the label is all letters, it's a roman numeral
            romans = list(itertools.islice(roman_nums(), 0, 50))
            return 1 + romans.index(label)
        else:
            return label
    else:
        m = re.match(r"([0-9]+)([\(])([a-z]+)([\)])", label, re.I) 
        return (int(m.groups()[0]), m.groups()[1])

def add_child(parent_node, node):
    "Add a child node to a parent, maintaining the order of the children."
    parent_node['children'].append(node)

    for c in parent_node['children']:
        if len(c['label']) == 5:
            c['sortable'] = make_label_sortable(c['label'][-1], roman=True)
        else:
            c['sortable'] = make_label_sortable(c['label'][-1])
                    
    parent_node['children'].sort(key=lambda x: x['sortable'])
