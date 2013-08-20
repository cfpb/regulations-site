import re
from regulations.generator import generator
from regulations.generator import node_types
from regulations.generator.reg import appendix_supplement


def get_labels(current):
    return current.split('-')


def get_toc(reg_part, version):
    creator = generator.LayerCreator()
    api_toc = creator.LAYERS[creator.TOC][0]
    toc = creator.get_layer_json(api_toc, reg_part, version)
    return toc


def up_level(labels):
    return '-'.join(labels[0:-1])


def is_last(i, l):
    return i+1 == len(l)


def choose_next_section(i, toc_up):
    if not is_last(i, toc_up):
        return toc_up[i+1]


def choose_previous_section(i, toc_up):
    if i > 0:
        return toc_up[i-1]


def nav_sections(current, version):
    labels = get_labels(current)
    reg_part = labels[0]
    toc = get_toc(reg_part, version)
    up = up_level(labels)

    if up in toc:
        for i, j in enumerate(toc[up]):
            if j['index'] == labels:
                next_section = choose_next_section(i, toc[up])
                previous_section = choose_previous_section(i, toc[up])

                return (previous_section, next_section)

def appendix_title(data):
    title_data = appendix_supplement(data)
    element = {
        'section': '-'.join(data['index']),
        'title': (title_data['label'], title_data['sub_label'])
    }
    return element
    
def section_title(data):
    if node_types.is_appendix(data['index']):
        return appendix_title(data)
    else:
        sect_number = '.'.join(data['index'])
        sect_text = re.search(sect_number + r'[^\w]*(.*)', data['title']).group(1)

        element = {
            'section': '-'.join(data['index']),
            'title': (sect_number, sect_text)
        }
        return element
