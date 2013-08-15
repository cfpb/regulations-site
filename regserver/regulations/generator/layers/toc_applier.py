#vim: set fileencoding=utf-8
import re

from regulations.generator.layers.internal_citation import InternalCitationLayer

class TableOfContentsLayer(object):
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
                    url = InternalCitationLayer.hash_url_for(data['index'],
                            self.version)
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
            element['sub_label'] = re.search(element['section'] 
                    + r'[^\w]*(.*)', data['title']).group(1)
    
    def appendix_supplement(self, element, data):
        """Handle items pointing to an appendix or supplement"""
        if len(data['index']) == 2 and data['index'][1].isalpha():
            if data['index'][1] == 'Interpretations':
                element['is_supplement'] = True
            else:
                element['is_appendix'] = True
            
            segments = self.try_split(data['title'], (u'—', '-'))
            if segments:
                element['label'], element['sub_label'] = segments


    def try_split(self, text, chars):
        """Utility method for splitting a string by one of multiple chars"""
        for c in chars:
            segments = text.split(c)
            if len(segments) > 1:
                return [s.strip() for s in segments]

