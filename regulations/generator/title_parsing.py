#vim: set fileencoding=utf-8
import re

from regulations.generator import node_types


def appendix_supplement(data):
    """Handle items pointing to an appendix or supplement"""
    node_type = node_types.type_from_label(data['index'])
    if len(data['index']) == 2 and node_type in (node_types.APPENDIX,
                                                 node_types.INTERP):
        element = {}
        if node_type == node_types.INTERP:
            element['is_supplement'] = True
        else:
            element['is_appendix'] = True

        segments = try_split(data['title'])
        if segments:
            element['label'], element['sub_label'] = segments[:2]
        elif '[' in data['title']:
            position = data['title'].find('[')
            element['label'] = data['title'][:position].strip()
            element['sub_label'] = data['title'][position:]
        else:
            element['label'] = data['title']

        element['section_id'] = '-'.join(data['index'])
        return element


def try_split(text, chars=(u'—', '-')):
    """Utility method for splitting a string by one of multiple chars"""
    for c in chars:
        segments = text.split(c)
        if len(segments) > 1:
            return [s.strip() for s in segments]


def section(data):
    """ Parse out parts of a section title. """
    if len(data['index']) == 2 and data['index'][1].isdigit():
        element = {}
        element['is_section'] = True
        element['label'] = '.'.join(data['index'])
        element['section_id'] = '-'.join(data['index'])

        # Due to inconsistencies in source data we need to be able to handle
        # several different possible section title formats:
        #
        # 1003.2 Something
        # § 1003.2 Something
        # Something
        # § Something
        #
        # In all of these cases, the sublabel should be "Something".
        title_no_label = data['title'].split(element['label'])[-1]
        sublabel_regex = re.compile(r'[^\w\[]*(.*)')
        element['sub_label'] = sublabel_regex.search(title_no_label).group(1)

        return element
