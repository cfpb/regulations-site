from regulations.generator.node_types import to_markup_id

class TableOfContentsLayer(object):
    def __init__(self, layer):
        self.layer = layer

    def apply_layer(self, text_index):
        if text_index in self.layer:
            layer_elements = self.layer[text_index]

            toc_list = []
            for element in layer_elements:
                element_url = to_markup_id(element['index']);
                toc_list.append({'url': "#%s" % "-".join(element_url),
                'label': element['title']})
            return ('TOC', toc_list)
