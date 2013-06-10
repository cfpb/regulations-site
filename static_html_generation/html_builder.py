#!/usr/bin/env python
#vim: set encoding=utf-8
from django.template import loader, Template, Context
from django.conf import settings
from layers.layers_applier import LayersApplier
from node_types import to_markup_id
import re
import settings as app_settings
from layers.layers_applier import LayersApplier
import re

class HTMLBuilder():
    header_regex = re.compile(ur'^(§)(\s*\d+\.\d+)(.*)$')

    def __init__(self, inline_applier, p_applier, search_applier):
        self.markup = u''
        self.sections = None
        self.tree = None
        self.inline_applier = inline_applier
        self.p_applier = p_applier
        self.search_applier = search_applier
        
    def generate_all_html(self):
        generate_html(self.tree[''])

    def generate_html(self):
        self.process_node(self.tree)

    def parse_doc_title(self, reg_title):
        match = re.search(r"[(].+[)]$", reg_title)
        if match:
            return match.group(0)

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
            node['header']  = node['label']['title']
            match = HTMLBuilder.header_regex.match(node['header'])
            if match:
                node['header_marker'] = match.group(1)
                node['header_num'] = match.group(2)
                node['header_title'] = match.group(3)

        node['label']['parts'] = to_markup_id(node['label']['parts'])
        node['markup_id'] = "-".join(node['label']['parts'])
        node['tree_level'] = len(node['label']['parts']) - 1

        node['node_type'] = self.node_type(node['tree_level'], node['label']['parts'])
        list_level, list_type = self.list_level(node['label']['parts'], node['node_type'])

        node['list_level'] = list_level
        node['list_type'] = list_type

        if len(node['text'].strip()):
            inline_elements = self.inline_applier.get_layer_pairs(node['label']['text'], node['text'])
            search_elements = self.search_applier.get_layer_pairs(node['label']['text'])

            layers_applier = LayersApplier()
            layers_applier.enqueue_from_list(inline_elements)
            layers_applier.enqueue_from_list(search_elements)

            node['marked_up'] = layers_applier.apply_layers(node['text'])

        node = self.p_applier.apply_layers(node)

        for c in node['children']:
            self.process_node(c)

    def get_title(self):
        titles = {
            'part': self.tree['label']['parts'][0],
            'reg_name': ''
        }
        reg_title = self.parse_doc_title(self.tree['label']['title'])
        if reg_title:
            titles['reg_name'] = reg_title
        return titles

    def render_markup(self):
        main_template = loader.get_template('simpler.html')
        c = Context({'tree':self.tree, 'titles': self.get_title(),
                        'GOOGLE_ANALYTICS_SITE':app_settings.GOOGLE_ANALYTICS_SITE, 
                        'GOOGLE_ANALYTICS_ID':app_settings.GOOGLE_ANALYTICS_ID})
        return main_template.render(c) 

class SlideDownInterpBuilder(HTMLBuilder):
    def render_markup(self):
        main_template = loader.get_template('slide-down-interp.html')
        c = Context({'node':self.tree})
        return main_template.render(c) 
