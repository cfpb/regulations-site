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

    def replace(self, xml_node, original, replacement):
        """ Helper method for replace_all(), this actually does the replace. This deals 
        with XML nodes, not nodes in the tree. """
        if xml_node.text:
            xml_node.text = xml_node.text.replace(original, replacement)

        for c in xml_node.getchildren():
            self.replace(c, original, replacement)

        if xml_node.tail:
            xml_node.tail = xml_node.tail.replace(original, replacement)

        return xml_node

    def location_replace(self, node, original, replacement, locations, counter=[0], offset_starter = [0]):
        if node.text:
            offsets = LayersApplier.find_all_offsets(original, node.text)
            cs = range(offset_starter[0], offset_starter[0] + len(offsets))
            d = {k:v for (k,v) in list(zip(cs, offsets))}

            while counter[0] < len(locations) and locations[counter[0]] in d:
                offsets = LayersApplier.find_all_offsets(original, node.text)
                d = {k:v for (k,v) in list(zip(cs, offsets))}

                offset = d[locations[counter[0]]]
                node.text = LayersApplier.replace_at_offset(offset, replacement, node.text)

                counter[0] += 1

            if len(cs) > 0:
                offset_starter[0] = cs[-1] + 1

        for c in node.getchildren():
            self.location_replace(c, original, replacement, locations, counter, offset_starter)

        if node.tail:
            offsets = LayersApplier.find_all_offsets(original, node.tail)
            cs = range(offset_starter[0], offset_starter[0] + len(offsets))
            d = {k:v for (k,v) in list(zip(cs, offsets))}

            while counter[0] < len(locations) and locations[counter[0]] in d:
                offsets = LayersApplier.find_all_offsets(original, node.tail)
                d = {k:v for (k,v) in list(zip(cs, offsets))}
                offset = d[locations[counter[0]]]
                node.tail = LayersApplier.replace_at_offset(offset, replacement, node.tail)
                counter[0] += 1

            if len(cs) > 0:
                offset_starter[0] = cs[-1] + 1
             
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

    @staticmethod
    def replace_at_offset(offset, replacement, text):
        return text[:offset[0]] + replacement + text[offset[1]:]

    @staticmethod
    def find_all_offsets(pattern, text):
        """ Return the start, end offsets for every occurrence of pattern in text. """
        return [(m.start(), m.end()) for m in re.finditer(re.escape(pattern.lower()), text.lower())]

    def replace_at(self, original, replacement, locations):
        """ Replace the occurrences of original at all the locations with replacement. """

        locations.sort()
        htmlized = html.fragment_fromstring(self.text, create_parent='div')
        self.location_replace(htmlized, original, replacement, locations, counter=[0], offset_starter=[0])
        self.text = html.tostring(htmlized)
        self.text = self.text.replace("<div>", "", 1)
        self.text = self.text[:self.text.rfind("</div>")]
        self.unescape_text()

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
            applied = layer.apply_layer_condensed(original_text, text_index)
            if applied:
                layer_pairs += applied
    
        #convert from offset-based to a search and replace layer. 
        layer_elements = []

        lower_original_text = original_text.lower()

        for o, r, offsets in layer_pairs:
            offset_locations = [(m.start(), m.end()) for m in re.finditer(re.escape(o.lower()), lower_original_text)]
            locations = [offset_locations.index(offset) for offset in offsets]
            layer_elements.append((o,r, locations))
        return layer_elements

        #for o, r, offsets in layer_pairs:
        #    offset_locations = [(m.start(), m.end()) for m in re.finditer(re.escape(o), original_text)] 
        #    locations = [offset_locations.index(offset)]
        #    layer_elements.append((o, r, locations))
        #if text_index == '1005-6-b-6':
        #    print layer_elements
        return layer_elements 

class ParagraphLayersApplier(LayersBase):
    """ Handle layers which apply to the whole paragraph. Layers include
    interpretations, section-by-section analyses, table of contents, etc."""

    def apply_layers(self, node):
        for layer in self.layers:
            pair = layer.apply_layer(node['markup_id'])
            if pair:
                node[pair[0]] = pair[1]
        return node
