import itertools


class AddQueue(object):
    """ Maintain a sorted list of nodes to add. This maintains a sorted queue
    of (label, node) tuples. """

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
        found_nodes = [n for n in self.queue if n[0] == label]
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

    def per_node(node):
        label_id = build_label(node)
        tree_hash[label_id] = node

        for c in node['children']:
            per_node(c)
    if tree:
        per_node(tree)
    return tree_hash


def parent_label(node):
    """This is not perfect. It can not handle children of subparts, for
    example"""
    if node['node_type'].upper() == 'INTERP':
        interpreting = list(itertools.takewhile(
            lambda l: l != 'Interp', node['label']))
        paragraph = node['label'][len(interpreting)+1:]
        if paragraph:
            return interpreting + ['Interp'] + paragraph[:-1]
        elif len(interpreting) == 1:    # Root of interpretations
            return interpreting
        else:
            return interpreting[:-1] + ['Interp']
    else:
        return node['label'][:-1]


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
    """ Make labels sortable, but converting them as appropriate.
    Also, appendices have labels that look like 30(a), we make those
    appropriately sortable. """

    if label.isdigit():
        return (int(label),)
    if roman:
        romans = list(itertools.islice(roman_nums(), 0, 50))
        return (1 + romans.index(label),)

    # segment the label piece into component parts
    # e.g. 45Ai33b becomes (45, 'A', 'i', 33, 'b')
    INT, UPPER, LOWER = 1, 2, 3
    segments, segment, seg_type = [], "", None
    for ch in label:
        if ch.isdigit():
            ch_type = INT
        elif ch.isalpha() and ch == ch.upper():
            ch_type = UPPER
        elif ch.isalpha() and ch == ch.lower():
            ch_type = LOWER
        else:
            # other character, e.g. parens, guarantee segmentation
            ch_type = None

        if ch_type != seg_type and segment:     # new type of character
            segments.append(segment)
            segment = ""

        seg_type = ch_type
        if ch_type:
            segment += ch

    if segment:    # ended with something other than a paren
        segments.append(segment)

    segments = [int(seg) if seg.isdigit() else seg for seg in segments]
    return tuple(segments)


def all_children_are_roman(parent_node):
    """
    Return true if all the children of the parent node have roman labels
    """
    romans = list(itertools.islice(roman_nums(), 0, 50))
    roman_children = [c['label'][-1] in romans
                      for c in parent_node['children']]
    return len(roman_children) > 0 and all(roman_children)


def add_child(parent_node, node):
    "Add a child node to a parent, maintaining the order of the children."

    children = parent_node['children']
    children.append(node)
    order = parent_node.get('child_labels', [])

    if (len(order) == len(children) and
            set(order) == set('-'.join(c['label']) for c in children)):
        lookup = {}
        for c in children:
            lookup['-'.join(c['label'])] = c
        parent_node['children'] = [lookup[label_id] for label_id in order]
    else:   # Explicit sort order not present/doesn't match nodes
        for c in parent_node['children']:
            if c['node_type'].upper() == 'INTERP':
                if c['label'][-1] == 'Interp':
                    sortable = make_label_sortable(
                        c['label'][-2], roman=(len(c['label']) == 6))
                else:
                    paragraph = list(itertools.dropwhile(
                        lambda l: l != 'Interp', c['label']))[1:]
                    sortable = make_label_sortable(
                        paragraph[-1], roman=(len(paragraph) == 2))

                if len(parent_node['label']) == 2:
                    #Highest interpretation node in the land
                    p = len(list(itertools.takewhile(lambda l: l != 'Interp',
                                                     c['label'])))
                    prefix_length = (p, )
                    sortable = prefix_length + sortable
                c['sortable'] = sortable
            elif c['node_type'].upper() == 'APPENDIX':
                roman_children = all_children_are_roman(parent_node)
                c['sortable'] = make_label_sortable(c['label'][-1],
                                                    roman=roman_children)

            else:
                c['sortable'] = make_label_sortable(
                    c['label'][-1], roman=(len(c['label']) == 5))

        parent_node['children'].sort(key=lambda x: x['sortable'])
