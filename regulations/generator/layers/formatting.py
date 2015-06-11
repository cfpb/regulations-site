from itertools import dropwhile, takewhile
import re

from django.template import loader, Context


class FormattingLayer(object):
    shorthand = 'formatting'

    def __init__(self, layer_data):
        self.layer_data = layer_data
        self.table_tpl = loader.get_template('regulations/layers/table.html')
        self.note_tpl = loader.get_template('regulations/layers/note.html')
        self.code_tpl = loader.get_template('regulations/layers/code.html')
        self.subscript_tpl = loader.get_template(
            'regulations/layers/subscript.html')
        self.dash_tpl = loader.get_template('regulations/layers/dash.html')

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

    def render_note(self, fence_data):
        lines = fence_data.get('lines', [])
        lines = [l for l in lines
                 if l.replace('Note:', '').replace('Notes:', '').strip()]
        context = Context({'lines': lines})
        return self.note_tpl.render(context).replace('\n', '')

    def render_code(self, fence_data):
        """Generic code rendering. Not language specific"""
        lines = fence_data.get('lines', [])
        context = Context({'lines': lines})
        return self.code_tpl.render(context)

    def apply_layer(self, text_index):
        """Convert all plaintext tables into html tables"""
        layer_pairs = []
        if text_index in self.layer_data:
            for data in self.layer_data[text_index]:
                if 'table_data' in data:
                    layer_pairs.append((data['text'],
                                        self.render_table(data['table_data']),
                                        data['locations']))

                if data.get('fence_data', {}).get('type') == 'note':
                    layer_pairs.append((data['text'],
                                        self.render_note(data['fence_data']),
                                        data['locations']))
                elif 'fence_data' in data:
                    layer_pairs.append((data['text'],
                                        self.render_code(data['fence_data']),
                                        data['locations']))

                if 'subscript_data' in data:
                    layer_pairs.append((
                        data['text'],
                        self.subscript_tpl.render(Context(
                            data['subscript_data'])).replace('\n', ''),
                        data['locations']))

                if 'dash_data' in data:
                    layer_pairs.append(
                            (data['text'], 
                             self.dash_tpl.render(
                                    Context(data['dash_data'])
                                ).replace('\n', ''),
                             data['locations']))

        return layer_pairs
