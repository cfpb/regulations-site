import re
import json
from lxml import html
from lxml.etree import ParserError
from Queue import PriorityQueue
from HTMLParser import HTMLParser

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

    def replace(self, node, original, replacement):
        """ Helper method for replace_all(), this actually does the replace. """
        if node.text:
            node.text = node.text.replace(original, replacement)

        for c in node.getchildren():
            self.replace(c, original, replacement)

        if node.tail:
            node.tail = node.tail.replace(original, replacement)

        return node

    def unescape_text(self):
        """ 
            Because of the way we do replace_all(), we need to 
            unescape HTML entities. 
        """
        self.text = HTMLParser().unescape(self.text)
            
    def replace_all(self, original, replacement):
        """ Replace all occurrences of original with replacement. This is HTML 
        aware. """

        htmlized = html.fragment_fromstring(self.text, create_parent='div')
        htmlized = self.replace(htmlized, original, replacement)
        self.text = html.tostring(htmlized)

        self.text = self.text.replace("<div>", "", 1)
        self.text = self.text[:self.text.rfind("</div>")]

        self.unescape_text()
        self.text = HTMLParser().unescape(self.text)

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

    def get_layer_pairs(self, text_index):
        elements = []
        for layer in self.layers:
            applied = layer.apply_layer(text_index)
            if applied:
                elements += applied
        return elements

class InlineLayersApplier(LayersBase):
    """ Apply multiple inline layers to given text (e.g. links,
    highlighting, etc.) """
    def __init__(self):
        LayersBase.__init__(self)
        self.original_text = None
        self.original_text_index = None
        self.modified_text = None

    def get_layer_pairs(self, text_index, original_text):
        layer_pairs = []
        for layer in self.layers:
            applied = layer.apply_layer(original_text, text_index)
            if applied:
                layer_pairs += applied

        layer_elements = [(o, r, []) for o, r in layer_pairs]
        return layer_elements 

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
