import types
import copy
from collections import deque

from regulations.generator.layers import tree_builder


class DiffApplier(object):
    """ Diffs between two versions of a regulation are represented in our
    particular JSON format. This class applies that diff to the older version
    of the regulation, generating HTML that clearly shows the changes between
    old and new. """

    INSERT = u'insert'
    DELETE = u'delete'
    DELETED_OP = 'deleted'
    ADDED_OP = 'added'

    def __init__(self, diff_json, label_requested):
        self.diff = diff_json
        #label_requested is the regulation label for which a diff is
        #requested.
        self.label_requested = label_requested

    def deconstruct_text(self, original):
        self.oq = [deque([c]) for c in original]

    def insert_text(self, pos, new_text):
        if pos == len(self.oq):
            self.oq[pos-1].extend(['<ins>', new_text, '</ins>'])
        else:
            self.oq[pos].appendleft('<ins>' + new_text + '</ins>')

    def delete_text(self, start, end):
        self.oq[start].appendleft('<del>')
        self.oq[end-1].append('</del>')

    def get_text(self):
        return ''.join([''.join(d) for d in self.oq])

    def delete_all(self, text):
        """ Mark all the text passed in as deleted. """
        return '<del>' + text + '</del>'

    def add_all(self, text):
        """ Mark all the text passed in as deleted. """
        return '<ins>' + text + '</ins>'

    def add_nodes_to_tree(self, original, adds):
        """ Add all the nodes from new_nodes into the original tree. """
        tree = tree_builder.build_tree_hash(original)

        for label, node in adds.queue:
            p_label = '-'.join(tree_builder.parent_label(node))
            if tree_builder.parent_in_tree(p_label, tree):
                tree_builder.add_node_to_tree(node, p_label, tree)
                adds.delete(label)
            else:
                parent = adds.find(p_label)
                if parent:
                    tree_builder.add_child(parent[1], node)
                else:
                    original.update(node)

    def is_child_of_requested(self, label):
        """ Return true if the label is a child of the requested label.  """
        req = self.label_requested
        if 'Interp' in label and 'Interp' in req:
            # Sub-paragraph
            if label.startswith(req + '-'):
                return True
            # The parent must not be a sub paragraph if the prefixes differ
            if not req.endswith('-Interp'):
                return False
            req_interpreting = req[:req.find('-Interp')]
            child_interpreting = label[:label.find('-Interp')]
            return child_interpreting.startswith(req_interpreting + '-')
        elif 'Interp' not in label and 'Interp' not in req:
            return label.startswith(req + '-')
        return False

    def relevant_added(self, label):
        """ Get the operations that add nodes, for the requested
        section/pargraph. """

        if (self.diff[label]['op'] == self.ADDED_OP
            and (label == self.label_requested
                 or self.is_child_of_requested(label))):
            return True

    def tree_changes(self, original_tree):
        """ Apply additions to the regulation tree. """

        def node(diff_node, label):
            """ Take diff's specification of a node, and actually turn it into
            a regulation node. """

            node = copy.deepcopy(diff_node)
            node['children'] = []
            if 'title' in node and node['title'] is None:
                del node['title']
            return node

        new_nodes = [(label, node(self.diff[label]['node'], label))
                     for label in self.diff if self.relevant_added(label)]

        adds = tree_builder.AddQueue()
        adds.insert_all(new_nodes)

        self.add_nodes_to_tree(original_tree, adds)

    def apply_diff_changes(self, original, diff_list):
        self.deconstruct_text(original)
        for d in diff_list:
            if d[0] == self.INSERT:
                _, pos, new_text = d
                self.insert_text(pos, new_text)
            if d[0] == self.DELETE:
                _, s, e = d
                self.delete_text(s, e)
            if isinstance(d[0], types.ListType):
                if d[0][0] == self.DELETE and d[1][0] == self.INSERT:
                    # Text replace scenario.
                    _, s, e = d[0]
                    self.delete_text(s, e)

                    _, _, new_text = d[1]

                    # Place the new text at the end of the delete for
                    # readability.
                    self.insert_text(e, new_text)
        return self.get_text()

    def apply_diff(self, original, label, component='text'):
        if label in self.diff:
            if self.diff[label]['op'] == self.DELETED_OP:
                return self.delete_all(original)
            if self.diff[label]['op'] == self.ADDED_OP:
                return self.add_all(original)
            if component in self.diff[label]:
                text_diffs = self.diff[label][component]
                return self.apply_diff_changes(original, text_diffs)
        return original
