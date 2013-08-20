#vim: set fileencoding=utf-8
import re

from regulations.generator.layers.internal_citation\
    import InternalCitationLayer
from regulations.generator import reg


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
                if self.sectional:
                    url = InternalCitationLayer.sectional_url_for(
                        data['index'], self.version)
                else:
                    url = InternalCitationLayer.hash_url_for(
                        data['index'], self.version)
                element = {
                    'url': url,
                    'label': data['title']
                }
                self.section(element, data)
                self.appendix_supplement(element, data)
                toc_list.append(element)
            return ('TOC', toc_list)

    def section(self, element, data):
        """Try to manipulate a section TOC item"""
        if len(data['index']) == 2 and data['index'][1].isdigit():
            element['is_section'] = True
            element['section'] = '.'.join(data['index'])
            element['sub_label'] = re.search(
                element['section'] + r'[^\w]*(.*)', data['title']).group(1)

    def appendix_supplement(self, element, data):
        as_data = reg.appendix_supplement(data)
        if as_data:
            element.update(as_data)
