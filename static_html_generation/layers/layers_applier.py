import re
import json
from lxml import html
from lxml.etree import ParserError
from Queue import PriorityQueue

class LayersApplier(object):
    """ Most layers replace content. We try to do this intelligently here, 
    so that layers don't step over each other. """

    def __init__(self):
        self.queue = PriorityQueue()
        self.text = None

    def enqueue_from_list(self, elements_list):
        for le in elements_list:
            self.enqueue(le)

    def enqueue(self, layer_element):
        original, replacement, locations = layer_element
        priority = len(original)
        item  = (original, replacement, locations)
        self.queue.put((-priority, item))

    def replace_all(self, original, replacement):
        """ Replace all occurrences of original with replacement. This is HTML 
        aware. """

        pre = self.text.find('<')
        post = self.text.rfind('>')
        
        if pre > -1 and post > -1:
            html_fragment = self.text[pre:post]
            prefix = self.text[:pre]
            postfix = self.text[post:]
            print html_fragment
            htmlized = html.fragment_fromstring(html_fragment)

            if htmlized.text:
                htmlized.text = htmlized.text.replace(original, replacement)

            for c in htmlized.getchildren():
                if c.text:
                    c.text = c.text.replace(original, replacement)

            self.text = prefix + html.tostring(htmlized) + postfix
        else:
            self.text = self.text.replace(original, replacement)

    def replace_at_offset(self, offset, replacement):
        self.text = self.text[:offset[0]] + replacement + self.text[offset[1]:]

    def find_all_offsets(self, pattern):
        """ Return the start, end offsets for every occurrence of pattern in text. """
        return [(m.start(), m.end()) for m in re.finditer(re.escape(pattern), self.text)]

    def replace_at(self, original, replacement, locations):
        """ Replace the occurrences of original at all the locations with replacement. """

        for l in locations:
            offsets = self.find_all_offsets(original)
            offset = offsets[l]
            self.replace_at_offset(offset, replacement)

    def apply_layers(self, original_text):
        self.text = original_text

        while not self.queue.empty():
            priority, layer_element  = self.queue.get()
            original, replacement, locations = layer_element

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

    def get_layer_pairs(self, text_index):
        elements = []
        for layer in self.layers:
            applied = layer.apply_layer(text_index)
            if applied:
                elements += applied
        return elements

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

    def get_layer_pairs(self, text_index, original_text):
        layer_pairs = []
        for layer in self.layers:
            applied = layer.apply_layer(original_text, text_index)
            if applied:
                layer_pairs += applied

        layer_elements = [(o, r, []) for o, r in layer_pairs]
        return layer_elements 

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
