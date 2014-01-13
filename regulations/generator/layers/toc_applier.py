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
                    toc_list.append(self.subpart(data))
                elif 'Interp' in data['index']:
                    toc_list.append(self.interp(data, toc_list))
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

    def interp(self, data, toc_list):
        """Expand the interp section of the TOC into subterps, collections of
        interpreted subparts, empty part, and appendices"""
        segments = title_parsing.try_split(data['title'])
        if not segments:
            segments = 'Supplement I', ''
        element = {
            'label': segments[0],
            'sub_label': segments[1],
            'index': data['index'],
            'section_id': '-'.join(data['index']),
            'is_supplement': True,
        }
        subterps = []
        found_subpart = False
        found_appendix = False
        for el in toc_list:
            if el.get('is_subpart'):
                found_subpart = True
                subterps.append({
                    'url': RegUrl.of(el['index'] + ['Interp'], self.version,
                                     self.sectional),
                    'label': el['label'],
                    'sub_label': el['sub_label'],
                    'index': el['index'] + ['Interp'],
                    'is_supplement': True,
                    'section_id': '-'.join(el['index']) + '-Interp'
                })
            elif el.get('is_appendix') and not found_appendix:
                found_appendix = True
                index = el['index'][:1] + ['Appendices', 'Interp']
                subterps.append({
                    'label': 'Appendices',
                    'url': RegUrl.of(index, self.version, self.sectional),
                    'index': index,
                    'is_supplement': True,
                    'section_id': '-'.join(index)
                })

        if not found_subpart:   # Add the empty subpart
            index = data['index'][:1] + ['Subpart', 'Interp']
            subterps.insert(0, {
                'label': 'Regulation Text',
                'index': index,
                'url': RegUrl.of(index, self.version, self.sectional),
                'is_supplement': True,
                'section_id': '-'.join(index)
            })

        element['sub_toc'] = subterps
        return element

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
