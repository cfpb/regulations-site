from itertools import dropwhile, takewhile
import re

from django.template import loader, Context


class FormattingLayer(object):
    shorthand = 'formatting'

    def __init__(self, layer_data):
        self.layer_data = layer_data
        self.table_tpl = loader.get_template('regulations/layers/table.html')

    def render_table(self, table):
        max_width = 0
        for header_row in table['header']:
            width = sum(cell['colspan'] for cell in header_row)
            max_width = max(max_width, width)
         
        #  Just in case a row is longer than the header
        row_max = max(len(row) for row in table['rows'])
        max_width = max(max_width, row_max)
         
        #  Now pad rows if needed
        for row in table['rows']:
            row.extend([''] * (max_width - len(row)))
            
        context = Context(table)
        #   Remove new lines so that they don't get escaped on display
        return self.table_tpl.render(context).replace('\n', '')

    def apply_layer(self, text_index):
        """Convert all plaintext tables into html tables"""
        layer_pairs = []
        if text_index in self.layer_data:
            for data in self.layer_data[text_index]:
                if 'table_data' in data:
                    layer_pairs.append((data['text'],
                                        self.render_table(data['table_data']),
                                        data['locations']))
        return layer_pairs
