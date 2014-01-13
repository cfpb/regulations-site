from regulations.generator import generator
from regulations.generator import node_types
from regulations.generator.node_types import type_from_label
from regulations.generator.title_parsing import appendix_supplement, section
from regulations.views import utils


def get_labels(current):
    return current.split('-')


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
    toc = utils.table_of_contents(reg_part, version, True)
    #   Flatten the hierarchy
    flat_toc = []
    for el in toc:
        if 'sub_toc' in el:
            flat_toc.extend(el['sub_toc'])
        else:
            flat_toc.append(el)
    #   Add prefixes
    for el in flat_toc:
        if el.get('is_section'):
            el['markup_prefix'] = '&sect;&nbsp;'
        elif el.get('is_subterp'):
            el['markup_prefix'] = 'Interpretations For '


    for idx, el in enumerate(flat_toc):
        if el['index'] == labels:
            if idx == 0:
                previous_section = None
            else:
                previous_section = flat_toc[idx - 1]

            if idx == len(flat_toc) - 1:
                next_section = None
            else:
                next_section = flat_toc[idx + 1]

            return (previous_section, next_section)
    # Implicit return None if the section isn't in the TOC
