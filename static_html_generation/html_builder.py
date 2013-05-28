#!/usr/bin/env python
from django.template import loader, Template, Context
from django.conf import settings
from node_types import NodeTypes
import settings as app_settings

class HTMLBuilder():
    def __init__(self, inline_applier, p_applier, search_applier):
        self.markup = u''
        self.sections = None
        self.tree = None
        self.inline_applier = inline_applier
        self.p_applier = p_applier
        self.search_applier = search_applier
        self.node_types = NodeTypes()
        
    def generate_all_html(self):
        generate_html(self.tree[''])

    def generate_html(self):
        self.process_node(self.tree)

    def list_level(self, parts, node_type):
        """ Return the list level and the list type. """
        if node_type == 'interpretation':
            level_type_map = {1:'1', 2:'i', 3:'A'}
            prefix_length = 4
        elif node_type == 'appendix':
            level_type_map = {1:'a', 2:'1', 3:'i', 4:'A'}
            prefix_length = 3
        elif node_type == 'regulation':
            level_type_map = {1:'a', 2:'1', 3:'i', 4:'A'}
            prefix_length = 2

        if len(parts) > prefix_length:
            list_level = len(parts) - prefix_length
            list_type = level_type_map[list_level]

            return (list_level, list_type)
        else:
            return (None, None)

    def node_type(self, tree_level, parts):
        """ A node in the regulation can be part of the appendix, the interpretation 
        section or simply the normal regulation text. We style them differently, hence we 
        need to distinguish between them. """
    
        if tree_level > 0:
            if parts[0] == 'I':
                return 'interpretation'
            else:
                level_two_id = parts[1]
                if level_two_id.isalpha():
                    return 'appendix'
                else:
                    return 'regulation'
        return 'regulation'

    def process_node(self, node):
        if 'title' in node['label']:
            node['markup_title']  = node['label']['title']

        node['label']['parts'] = self.node_types.change_type_names(node['label']['parts'])
        node['markup_id'] = "-".join(node['label']['parts'])
        node['tree_level'] = len(node['label']['parts']) - 1

        node['node_type'] = self.node_type(node['tree_level'], node['label']['parts'])
        list_level, list_type = self.list_level(node['label']['parts'], node['node_type'])

        node['list_level'] = list_level
        node['list_type'] = list_type

        if len(node['text'].strip()):
            #   Use the Tree's ID
            node['marked_up'] = self.inline_applier.apply_layers(
                    node['text'], node['label']['text'])
            node['marked_up'] = self.search_applier.apply_layers(
                    node['marked_up'], node['label']['text'])

        node = self.p_applier.apply_layers(node)

        for c in node['children']:
            self.process_node(c)

    def render_markup(self, f=None):
        main_template = loader.get_template('simpler.html')
        c = Context({'tree':self.tree, 
                        'GOOGLE_ANALYTICS_SITE':app_settings.GOOGLE_ANALYTICS_SITE, 
                        'GOOGLE_ANALYTICS_ID':app_settings.GOOGLE_ANALYTICS_ID})
        return main_template.render(c) 
