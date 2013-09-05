def build_tree_hash(tree):
    """ Build a hash map of a tree's nodes, so that we don't 
    have to keep walking the tree. """
    tree_hash = {}
    tree_hash[tree['label_id']] = original

    for c in tree['children']:
        tree_hash[c['label_id']] = c
    return tree

def parent_in_tree(node_label, tree_hash):
    """ Return True if the parent of node_label is in the tree """
    parent_label = node_label.rsplit("-", 1)[0]
    return parent_label in tree_hash

def add_node_to_tree(node, tree_hash):
    """ Add the node to the tree """
    pass
