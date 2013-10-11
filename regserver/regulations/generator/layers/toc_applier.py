#vim: set fileencoding=utf-8
import re

from regulations.generator.layers.utils import RegUrl
from regulations.generator import title_parsing


class TableOfContentsLayer(object):
    shorthand = 'toc'

    def __init__(self, layer):
        self.layer = layer
        self.sectional = False
        self.version = None

    def apply_layer(self, text_index):
        if text_index in self.layer:
            layer_elements = self.layer[text_index]

            toc_list = []
            for data in layer_elements:
                element = {
                    'url': RegUrl.of(data['index'], self.version,
                                     self.sectional),
                    'label': data['title'],
                    'index': data['index'],
                    'section_id': '-'.join(data['index'])
                }
                self.section(element, data)
                self.appendix_supplement(element, data)
                toc_list.append(element)
            return ('TOC', toc_list)

    @staticmethod
    def section(element, data):
        title_data = title_parsing.section(data)
        if title_data:
            element.update(title_data)

    @staticmethod
    def appendix_supplement(element, data):
        as_data = title_parsing.appendix_supplement(data)
        if as_data:
            element.update(as_data)
