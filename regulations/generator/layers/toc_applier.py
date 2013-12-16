#vim: set fileencoding=utf-8
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
            seen_appendix = False
            for data in layer_elements:
                if 'Subpart' in data['index']:
                    element = self.subpart(data)
                    toc_list.append(element)
                else:
                    element = {
                        'url': RegUrl.of(data['index'], self.version,
                                         self.sectional),
                        'label': data['title'],
                        'index': data['index'],
                        'section_id': '-'.join(data['index'])
                    }
                    self.section(element, data)
                    self.appendix_supplement(element, data, seen_appendix)
                    toc_list.append(element)
                    seen_appendix = seen_appendix or element.get('is_appendix')
            return ('TOC', toc_list)

    def subpart(self, data):
        element = {
            'label': ' '.join(data['index'][1:]),
            'sub_label': data['title'],
            'index': data['index'],
            'section_id': '-'.join(data['index']),
            'is_subpart': True
        }
        result = self.apply_layer('-'.join(data['index']))
        if result:
            element['sub_toc'] = result[1]
        return element

    @staticmethod
    def section(element, data):
        title_data = title_parsing.section(data)
        if title_data:
            element.update(title_data)

    @staticmethod
    def appendix_supplement(element, data, seen_appendix=False):
        as_data = title_parsing.appendix_supplement(data)
        if as_data:
            element.update(as_data)
        if element.get('is_appendix'):
            element['is_first_appendix'] = not seen_appendix
