from lxml import html
from Queue import PriorityQueue
from HTMLParser import HTMLParser

from regulations.generator.layers.location_replace import LocationReplace

import logging

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
        item = (original, replacement, locations)
        self.queue.put((-priority, item))

    def replace(self, xml_node, original, replacement):
        """ Helper method for replace_all(), this actually does the replace.
        This deals with XML nodes, not nodes in the tree. """
        if xml_node.text:
            xml_node.text = xml_node.text.replace(original, replacement)

        for c in xml_node.getchildren():
            self.replace(c, original, replacement)

        if xml_node.tail:
            xml_node.tail = xml_node.tail.replace(original, replacement)

        return xml_node

    def location_replace(self, xml_node, original, replacement, locations):
        LocationReplace().location_replace(xml_node, original, replacement,
                                           locations)

    def unescape_text(self):
        """ Because of the way we do replace_all(), we need to unescape HTML
        entities.  """
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

    def replace_at(self, original, replacement, locations):
        """ Replace the occurrences of original at all the locations with
        replacement. """

        locations.sort()
        self.text = LocationReplace().location_replace_text(
            self.text, original, replacement, locations)
        self.unescape_text()

    def apply_layers(self, original_text):
        self.text = original_text

        while not self.queue.empty():
            priority, layer_element = self.queue.get()
            original, replacement, locations = layer_element

            if not locations:
                self.replace_all(original, replacement)
            else:
                self.replace_at(original, replacement, locations)

        return self.text


class LayersBase(object):
    """ Base class which keeps track of multiple laeyrs. """
    def __init__(self):
        self.layers = {}

    def add_layer(self, layer):
        self.layers[layer.__class__.shorthand] = layer


class SearchReplaceLayersApplier(LayersBase):
    def __init__(self):
        LayersBase.__init__(self)
        self.original_text = None
        self.modified_text = None

    def get_layer_pairs(self, text_index):
        elements = []
        for layer in self.layers.values():
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
        for layer in self.layers.values():
            applied = layer.apply_layer(original_text, text_index)
            if applied:
                layer_pairs += applied

        #convert from offset-based to a search and replace layer.
        layer_elements = []

        for o, r, offset in layer_pairs:
            offset_locations = LocationReplace.find_all_offsets(o,
                                                                original_text)
            try:
                locations = [offset_locations.index(offset)]
                layer_elements.append((o, r, locations))
            except Exception as ex:
                logging.info('{0!s}'.format(ex))
                logging.info('Problem interpolating offsets: {0}, {1}'.format(offset_locations, offset))
        return layer_elements


class ParagraphLayersApplier(LayersBase):
    """ Handle layers which apply to the whole paragraph. Layers include
    interpretations, section-by-section analyses, table of contents, etc."""

    def apply_layers(self, node):
        for layer in self.layers.values():
            pair = layer.apply_layer(node['markup_id'])
            if pair:
                node[pair[0]] = pair[1]
        return node
