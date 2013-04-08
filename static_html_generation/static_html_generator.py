#!/usr/bin/env python

import codecs
import json

from django.template import loader, Template, Context
from django.conf import settings

import api_stub
from layers_applier import LayersApplier

class HTMLBuilder():
    def __init__(self, layers_applier):
        self.markup = u''
        self.sections = None
        self.tree = None
        self.layers_applier = layers_applier
        
        settings.configure(TEMPLATE_DEBUG=False, 
            TEMPLATE_LOADERS=('django.template.loaders.filesystem.Loader',), 
            TEMPLATE_DIRS = ('templates/',))

    def generate_html(self):
        self.process_node(self.tree)

    def process_node(self, node):
        if 'title' in node['label']:
            node['markup_title']  = node['label']['title']

        node['markup_id'] = "-".join(node['label']['parts'])
        node['tree_level'] = len(node['label']['parts']) - 1

        node['marked_up'] = self.layers_applier.apply_layers(node['text'], node['markup_id'])

        for c in node['children']:
            self.process_node(c)

    def render_markup(self, f=None):
        main_template = loader.get_template('simpler.html')
        c = Context({'tree':self.tree})
        return main_template.render(c) 

def write_file(filename, markup):
    f = codecs.open(filename, 'w', encoding='utf-8')
    f.write(markup)
    f.close()

if __name__ == "__main__":
    reg_json = api_stub.get_regulation_as_json('regulations/rege/rege.json')

    from external_citation import ExternalCitationLayer
    el = json.load(open('regulations/rege/external_citations_layer.json'))

    layers_applier = LayersApplier()
    layers_applier.add_layer(ExternalCitationLayer(el))
    
    makers_markup = HTMLBuilder(layers_applier)
    makers_markup.tree = reg_json
    makers_markup.generate_html()
    markup = makers_markup.render_markup()

    write_file('/tmp/rege.html', markup)
