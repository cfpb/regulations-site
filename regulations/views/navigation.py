from regulations.generator.section_url import SectionUrl
from regulations.generator.toc import fetch_toc


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


def _add_extra(el, version):
    """Add extra fields to a TOC element -- only added to elements we will
    use for prev/next"""
    if el.get('is_section'):
        el['markup_prefix'] = '&sect;&nbsp;'
    elif el.get('is_subterp'):
        el['markup_prefix'] = 'Interpretations For '
    el['url'] = SectionUrl.of(el['index'], version, sectional=True)
    return el


def nav_sections(current, version):
    labels = get_labels(current)
    reg_part = labels[0]
    toc = fetch_toc(reg_part, version, flatten=True)
    for idx, el in enumerate(toc):
        if el['index'] == labels:
            if idx == 0:
                previous_section = None
            else:
                previous_section = _add_extra(toc[idx - 1], version)

            if idx == len(toc) - 1:
                next_section = None
            else:
                next_section = _add_extra(toc[idx + 1], version)

            return (previous_section, next_section)
    # Implicit return None if the section isn't in the TOC
