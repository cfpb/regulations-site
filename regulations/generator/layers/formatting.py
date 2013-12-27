from itertools import dropwhile, takewhile
import re

from django.template import loader, Context


def _may_be_row(line):
    return line.startswith('|') and line.endswith('|')


_not_row = lambda txt: not _may_be_row(txt)


_divider_re = re.compile(r'^\-{3}\-*$')


def _verify_table_lines(lines):
    table = [txt.split('|') for txt in lines]   # split into cells
    if len(table) > 2:  # header + divider + row
        header, divider = table[:2]

        #   divider looks right, all rows are the same length
        if (all(_divider_re.match(div) for div in divider[1:-1])
                and all(len(row) == len(header) for row in table)):
            return table


class TableLayer(object):
    shorthand = 'formatting'

    def __init__(self):
        self.template = loader.get_template('regulations/layers/table.html')

    def rendered_triplet(self, table):
        text = '\n'.join('|'.join(row) for row in table)

        table = [row[1:-1] for row in table]    # remove outer pipes
        header, divider = table[:2]
        context = Context({'header': header, 'rows': table[2:]})
        return (text, self.template.render(context).strip('\n'), 0)

    def apply_layer(self, text, text_index):
        """Convert all plaintext tables into html tables"""
        lines = text.split('\n')
        lines = list(dropwhile(_not_row, lines))

        tables = []
        while lines:
            table_lines = list(takewhile(_may_be_row, lines))
            table = _verify_table_lines(table_lines)
            if table:
                tables.append(table)

            lines = lines[len(table_lines):]
            lines = list(dropwhile(_not_row, lines))

        return [self.rendered_triplet(table) for table in tables]
