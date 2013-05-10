#!/usr/bin/env python

from django.template import loader, Template, Context
from django.conf import settings
from node_types import NodeTypes
import settings as app_settings

class HTMLBuilder():
    def __init__(self, layers_applier, toc_applier):
        self.markup = u''
        self.sections = None
        self.tree = None
        self.layers_applier = layers_applier
        self.toc_applier = toc_applier
        self.node_types = NodeTypes()
        
    def generate_all_html(self):
        generate_html(self.tree[''])

    def generate_html(self):
        self.process_node(self.tree)

    def node_type(self, tree_level, parts):
        """ A node in the regulation can be part of the appendix, the interpretation 
        section or simply the normal regulation text. We style them differently, hence we 
        need to distinguish between them. """

        if tree_level > 0:
            level_two_id = parts[1]

            if level_two_id == 'Interpretations':
                return 'interpretation'
            elif level_two_id.isalpha():
                return 'appendix'
            else:
                return 'regulation'

    def process_node(self, node):
        if 'title' in node['label']:
            node['markup_title']  = node['label']['title']

        node['markup_id'] = self.node_types.change_type_names(node['label']['parts'])
        node['tree_level'] = len(node['label']['parts']) - 1

        node['node_type'] = self.node_type(node['tree_level'], node['label']['parts'])

        if len(node['text'].strip()):
            node['marked_up'] = self.layers_applier.apply_layers(node['text'], node['markup_id'])

        toc = self.toc_applier.apply_layer(node['markup_id'])

        if toc:
            node[toc[0]] = toc[1]

        for c in node['children']:
            self.process_node(c)

    def render_markup(self, f=None):
        main_template = loader.get_template('simpler.html')
        c = Context({'tree':self.tree, 
                        'GOOGLE_ANALYTICS_SITE':app_settings.GOOGLE_ANALYTICS_SITE, 
                        'GOOGLE_ANALYTICS_ID':app_settings.GOOGLE_ANALYTICS_ID})
        return main_template.render(c) 
