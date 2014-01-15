"""The table of contents needed isn't quite the same as the toc provided by
the api. We need to modify it a bit to group subparts, subterps, etc. These
modifications, then, are used for navigation, citations, and the TOC
layer"""
from regulations.generator import title_parsing
from regulations.generator.api_reader import ApiReader


def fetch_toc(reg_part, version, flatten=False):
    """Fetch the toc, transform it into a list usable by navigation, etc."""
    api = ApiReader()
    toc = api.layer('toc', reg_part, version)

    toc_list = []
    for data in toc[reg_part]:
        if 'Subpart' in data['index']:
            toc_list.append(toc_subpart(data, toc_list, toc))
        elif 'Interp' in data['index']:
            toc_list.append(toc_interp(data, toc_list))
        else:
            toc_list.append(toc_sect_appendix(data, toc_list))
    if flatten:
        flattened = []
        for el in toc_list:
            if 'sub_toc' in el:
                flattened.extend(el['sub_toc'])
            else:
                flattened.append(el)
        return flattened
    return toc_list


def toc_sect_appendix(data, so_far):
    """Transforms normal sections and appendices"""
    title_data = title_parsing.section(data)
    if title_data:
        data.update(title_data)

    title_data = title_parsing.appendix_supplement(data)
    if title_data:
        data.update(title_data)

    if data.get('is_appendix'):
        seen_appendix = any(el.get('is_appendix') for el in so_far)
        data['is_first_appendix'] = not seen_appendix
    return data


def toc_subpart(data, so_far, toc):
    """Transforms a subpart, giving it sectional children"""
    element = {
        'label': ' '.join(data['index'][1:]),
        'sub_label': data['title'],
        'index': data['index'],
        'section_id': '-'.join(data['index']),
        'is_subpart': True,
        'sub_toc': []
    }
    for sub in toc['-'.join(data['index'])]:
        element['sub_toc'].append(toc_sect_appendix(sub, so_far))
    return element


def toc_interp(data, so_far):
    """Transforms a subpart, expanding it into subterps (collections of
    interpreted subparts, empty part, and appendices"""
    segments = title_parsing.try_split(data['title'])
    if not segments:
        segments = 'Supplement I', ''
    element = {
        'label': segments[0],
        'sub_label': segments[1],
        'index': data['index'],
        'section_id': '-'.join(data['index']),
        'is_supplement': True,
        'sub_toc': []
    }
    found_subpart = False
    found_appendix = False
    for el in so_far:
        if el.get('is_subpart'):
            found_subpart = True
            index = el['index'] + ['Interp']
            element['sub_toc'].append({
                'label': el['label'],
                'sub_label': el['sub_label'],
                'index': index,
                'is_subterp': True,
                'section_id': '-'.join(index)
            })
        elif el.get('is_appendix') and not found_appendix:
            found_appendix = True
            index = el['index'][:1] + ['Appendices', 'Interp']
            element['sub_toc'].append({
                'label': 'Appendices',
                'index': index,
                'is_subterp': True,
                'section_id': '-'.join(index)
            })

    if not found_subpart:   # Add the empty subpart
        index = data['index'][:1] + ['Subpart', 'Interp']
        element['sub_toc'].insert(0, {
            'label': 'Regulation Text',
            'index': index,
            'is_subterp': True,
            'section_id': '-'.join(index)
        })
    return element
