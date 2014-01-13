from regulations.generator import generator
from regulations.generator import node_types
from regulations.generator.node_types import type_from_label
from regulations.generator.title_parsing import appendix_supplement, section


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
        #   Flatten the hierarchy
        siblings = []
        for el in toc[up]:
            if 'Subpart' in el['index']:
                siblings.extend(toc['-'.join(el['index'])])
            else:
                siblings.append(el)

        for idx, el in enumerate(siblings):
            if el['index'] == labels:
                next_section = choose_next_section(idx, siblings)
                previous_section = choose_previous_section(idx, siblings)

                return (previous_section, next_section)


def parse_section_title(data):
    """ Separate the section number from the section title (this works for
    both appendix and section text. """

    if type_from_label(data['index']) in (node_types.APPENDIX,
                                          node_types.INTERP):
        return appendix_supplement(data)
    else:
        return section(data)
