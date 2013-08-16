#!/usr/bin/env python
#vim: set fileencoding=utf-8
import re

from django.template import loader, Context
from itertools import ifilter, ifilterfalse

from node_types import to_markup_id, APPENDIX, INTERP
from layers.layers_applier import LayersApplier


class HTMLBuilder():
    header_regex = re.compile(ur'^(§&nbsp;)(\s*\d+\.\d+)(.*)$')
    section_number_regex = re.compile(ur"(§+)\s+")

    def __init__(self, inline_applier, p_applier, search_applier):
        self.markup = u''
        self.sections = None
        self.tree = None
        self.inline_applier = inline_applier
        self.p_applier = p_applier
        self.search_applier = search_applier

    def generate_all_html(self):
        self.generate_html(self.tree[''])

    def generate_html(self):
        self.process_node(self.tree)

    def parse_doc_title(self, reg_title):
        match = re.search(r"[(].+[)]$", reg_title)
        if match:
            return match.group(0)

    @staticmethod
    def section_space(text):
        """ After a section sign, insert a non-breaking space. """
        return HTMLBuilder.section_number_regex.sub(ur'\1&nbsp;', text)

    def list_level(self, parts, node_type):
        """ Return the list level and the list type. """
        if node_type == INTERP:
            level_type_map = {1: '1', 2: 'i', 3: 'A'}
            prefix_length = parts.index('Interp')+1
        elif node_type == APPENDIX:
            level_type_map = {1: 'a', 2: '1', 3: 'i', 4: 'A'}
            prefix_length = 3
        else:
            level_type_map = {1: 'a', 2: '1', 3: 'i', 4: 'A'}
            prefix_length = 2

        if len(parts) > prefix_length:
            list_level = len(parts) - prefix_length
            list_type = level_type_map[list_level]

            return (list_level, list_type)
        else:
            return (None, None)

    def process_node(self, node):
        if 'title' in node:
            node['header'] = node['title']
            node['header'] = HTMLBuilder.section_space(node['header'])
            match = HTMLBuilder.header_regex.match(node['header'])
            if match:
                node['header_marker'] = match.group(1)
                node['header_num'] = match.group(2)
                node['header_title'] = match.group(3)

        node['text'] = node['text'].rstrip()
        node['label_id'] = '-'.join(node['label'])
        node['html_label'] = to_markup_id(node['label'])
        node['markup_id'] = "-".join(node['html_label'])
        node['tree_level'] = len(node['label']) - 1

        list_level, list_type = self.list_level(
            node['label'], node['node_type'])

        node['list_level'] = list_level
        node['list_type'] = list_type

        if len(node['text']):
            inline_elements = self.inline_applier.get_layer_pairs(
                node['label_id'], node['text'])
            search_elements = self.search_applier.get_layer_pairs(
                node['label_id'])

            layers_applier = LayersApplier()
            layers_applier.enqueue_from_list(inline_elements)
            layers_applier.enqueue_from_list(search_elements)

            node['marked_up'] = layers_applier.apply_layers(node['text'])
            node['marked_up'] = HTMLBuilder.section_space(node['marked_up'])

        node = self.p_applier.apply_layers(node)

        if 'TOC' in node:
            for l in node['TOC']:
                l['label'] = HTMLBuilder.section_space(l['label'])

        if 'interp' in node and 'markup' in node['interp']:
            node['interp']['markup'] = HTMLBuilder.section_space(
                node['interp']['markup'])

        if node['node_type'] == INTERP:
            self.modify_interp_node(node)

        for c in node['children']:
            self.process_node(c)

    def modify_interp_node(self, node):
        """Add extra fields which only exist on interp nodes"""
        #   ['105', '22', 'Interp'] => section header
        node['section_header'] = len(node['label']) == 3

        is_header = lambda child: child['label'][-1] == 'Interp'
        node['header_children'] = list(ifilter(is_header, node['children']))
        node['par_children'] = list(ifilterfalse(is_header, node['children']))

    def get_title(self):
        titles = {
            'part': self.tree['label'][0],
            'reg_name': ''
        }
        reg_title = self.parse_doc_title(self.tree['title'])
        if reg_title:
            titles['reg_name'] = reg_title
        return titles


class SlideDownInterpBuilder(HTMLBuilder):
    def render_markup(self):
        main_template = loader.get_template('slide-down-interp.html')
        c = Context({'node': self.tree})
        return main_template.render(c)
