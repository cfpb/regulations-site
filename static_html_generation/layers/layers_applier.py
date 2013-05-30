import re
import json
from Queue import PriorityQueue

class LayersApplier(object):
    """ Most layers replace content. We try to do this intelligently here, 
    so that layers don't step over each other. """

    def __init__(self):
        self.queue = PriorityQueue()
        self.text = None

    def enqueue(self, original, replacement, locations):
        priority = len(original)
        item  = (original, replacement, locations)
        self.queue.put((-priority, item))

    def replace_all(original, replacement):
        """ Replace all occurrences of original with replacement. """
        self.modified_text = self.text.replace(original, replacement)

    def find_all_offsets(self, pattern):
        """ Return the start, end offsets for every occurrence of pattern in text. """
        return [(m.start(), m.end()) for m in re.finditer(re.escape(pattern), text)]

    def replace_at(original, replacement, locations):
        """ Replace the occurrences of original at all the locations with replacement. """
        offset = offsets[l]
        self.modified_text = self.replace_at_offset(offset, self.modified_text, phrase_replacement)

    def apply_layers(self, original_text):
        self.text = original_text

        while not self.queue.empty():
            original, replacement, locations = layer_item = self.queue.get()

            if not locations:
                self.replace_all(original, replacement)
            else:
                self.replace_at(original, replacement, locations)

        return self.text

class LayersBase(object):
    """ Base class which keeps track of multiple laeyrs. """
    def __init__(self):
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)

class SearchReplaceLayersApplier(LayersBase):
    def __init__(self):
        LayersBase.__init__(self)
        self.original_text = None
        self.modified_text = None

    def replace_at_offset(self, offset, text, replacement):
        modified_text = text[:offset[0]] + replacement + text[offset[1]:]
        return modified_text

    def find_all_offsets(self, pattern, text):
       " Return the start, end offsets for every occurrence of pattern in text. "
       return  [(m.start(), m.end()) for m in re.finditer(re.escape(pattern), text)]

    def apply_layers(self, original_text, text_index):
        self.original_text = original_text
        self.modified_text = original_text
        self.original_text_index = text_index

        for layer in self.layers:
            elements = layer.apply_layer(self.original_text_index)

            for el in elements:
                phrase, phrase_replacement, locations = el
                offsets = self.find_all_offsets(phrase, self.modified_text)

                for l in locations:
                    print 'PHRASE |%s|' % phrase
                    print 'MODIFIED TEXT: %s' % self.modified_text
                    print offsets
                    offset = offsets[l]
                    self.modified_text = self.replace_at_offset(offset, self.modified_text, phrase_replacement)
        return self.modified_text

class InlineLayersApplier(LayersBase):
    """ Apply multiple inline layers to given text (e.g. links,
    highlighting, etc.) """
    def __init__(self):
        LayersBase.__init__(self)
        self.original_text = None
        self.original_text_index = None
        self.modified_text = None

    def apply_layers(self, original_text, text_index):
        self.original_text = original_text
        self.modified_text = original_text
        self.original_text_index = text_index

        for layer in self.layers:
            layer_pairs = layer.apply_layer(self.original_text,
                    self.original_text_index)
            if layer_pairs:
                self.apply_pairs(layer_pairs)
        return self.modified_text

    def apply_pairs(self, pairs):
        """ Inline Layers return pairs of (search term, replacement text).
        Modify the text for each pair. """
        for old, new in pairs:
            self.modified_text = self.modified_text.replace(old, new)

class ParagraphLayersApplier(LayersBase):
    """ Handle layers which apply to the whole paragraph. Layers include
    interpretations, section-by-section analyses, table of contents, etc."""

    def __init__(self, reg_tree):
        """The regulation tree can be useful to layers (e.g.
        interpretations), so we pass that along"""
        LayersBase.__init__(self)
        self.reg_tree = reg_tree

    def apply_layers(self, node):
        for layer in self.layers:
            pair = layer.apply_layer(node['markup_id'], self.reg_tree)
            if pair:
                node[pair[0]] = pair[1]
        return node
