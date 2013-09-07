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


def build_tree_hash(tree):
    """ Build a hash map of a tree's nodes, so that we don't 
    have to keep walking the tree. """
    tree_hash = {}

    if tree:
        tree_hash[tree['label_id']] = tree

        for c in tree['children']:
            tree_hash[c['label_id']] = c
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

def add_child(parent_node, node):
    "Add a child node to a parent, maintaining the order of the children."
    parent_node['children'].append(node)
    parent_node['children'].sort(key=lambda x: x['label'][-1])
