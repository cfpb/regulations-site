from itertools import takewhile

from regulations.generator.node_types import label_to_text
from regulations.generator.layers.tree_builder import make_label_sortable


def sort_regtext_label(label):
    """ Make a regtext label sortable """
    sortable = [make_label_sortable(l)[0] for l in label]
    if len(sortable) > 4:
        sortable[4] = make_label_sortable(sortable[4], roman=True)[0]
    return sortable


def sort_analyses(analyses):
    """ Sort the labels, so that the list of section-by-section analyses
    can be displayed in the correct order. """
    if analyses:
        for a in analyses:
            label = a['label_id'].split('-')
            if 'Interp' not in a['label_id']:
                sortable = sort_regtext_label(label)
            else:
                prefix = label[:label.index('Interp')]
                suffix = label[label.index('Interp') + 1:]

                prefix_sortable = sort_regtext_label(prefix)

                suffix_sortable = [make_label_sortable(l)[0] for l in suffix]
                if len(suffix_sortable) > 1:
                    suffix_sortable[1] = make_label_sortable(
                        suffix_sortable[1], roman=True)[0]
                sortable = prefix_sortable + suffix_sortable
            a['sortable'] = tuple(sortable)
        sorted_analyses = sorted(analyses, key=lambda a: a['sortable'])
        for a in sorted_analyses:
            if 'sortable' in a:
                del a['sortable']
        return sorted_analyses


class SectionBySectionLayer(object):
    shorthand = 'sxs'

    def __init__(self, layer):
        self.layer = layer
        # Perform the computations we'll use when applying the layer only once
        self.precomputations = {}
        for key in layer:
            key_parts = key.split('-')

            # Interpretations have an added complication:
            # 1005-2-Interp-2 is a child of 1005-Interp
            key_prefix = list(takewhile(lambda k: k != 'Interp', key_parts))
            self.precomputations[key] = (key_parts, key_prefix,
                                         'Interp' in key_parts)

    def to_template_dict(self, key):
        """Take the reference associated with this SxS and turn it into data
        which can be used in the template"""
        # We care only about the latest
        doc_number, label_id = self.layer[key][-1]['reference']
        return [{'doc_number': doc_number,
                 'label_id': label_id,
                 'text': label_to_text(label_id.split('-'),
                                       include_section=False,
                                       include_marker=True)}]

    def apply_layer(self, text_index):
        """Return a pair of field-name + analyses if they apply; include all
        children"""
        analyses = []
        requested = text_index.split('-')
        requested_prefix = list(takewhile(lambda k: k != 'Interp', requested))

        for key in self.layer:
            key_parts, key_prefix, key_is_interp = self.precomputations[key]
            key_prefix = key_prefix[:len(requested_prefix)]
            if (requested[-1] == 'Interp' and key_prefix == requested_prefix
                    and key_is_interp):
                analyses.extend(self.to_template_dict(key))

            # Simple Case: lexical child
            elif (key_parts[:len(requested)] == requested
                  and ('Interp' in requested) == key_is_interp):
                analyses.extend(self.to_template_dict(key))

        analyses = sort_analyses(analyses)
        if analyses:
            return 'analyses', analyses
