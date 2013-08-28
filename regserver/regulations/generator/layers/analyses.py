from itertools import takewhile

from regulations.generator.node_types import label_to_text


class SectionBySectionLayer(object):
    shorthand = 'sxs'

    def __init__(self, layer):
        self.layer = layer

    def to_template_dict(self, key):
        """Take the reference associated with this SxS and turn it into data
        which can be used in the template"""
        # We care only about the latest
        doc_number, label_id = self.layer[key][-1]['reference']
        return [{'doc_number': doc_number,
                 'label_id': label_id,
                 'text': label_to_text(label_id.split('-'))}]

    def apply_layer(self, text_index):
        """Return a pair of field-name + analyses if they apply; include all
        children"""
        analyses = []
        for key in self.layer:
            requested = text_index.split('-')
            key_parts = key.split('-')

            # Simple Case: lexical child
            if key_parts[:len(requested)] == requested:
                analyses.extend(self.to_template_dict(key))

            # Interpretations have an added complication
            key_prefix = takewhile(lambda k: k != 'Interp', key_parts)
            key_prefix = list(key_prefix)[:len(requested)]
            if requested[-1] == 'Interp' and requested[:-1] == key_prefix:
                analyses.extend(self.to_template_dict(key))

        if analyses:
            return 'analyses', sorted(analyses, key=lambda a: a['label_id'])
