"""The table of contents needed isn't quite the same as the toc provided by
the api. We need to modify it a bit to group subparts, subterps, etc. These
modifications, then, are used for navigation, citations, and the TOC
layer"""
from regulations.generator import title_parsing
from regulations.generator.api_reader import ApiReader

# Sometimes the reg has interps for the regtext but NOT for the appendices,
# even though the appendices exist. Unfortunately the logic here appears to
# render a TOC entry for interps to appendices whenever an appendix is present
# at all, regardless of whether it has interps or not. This is obviously wrong
# but so deeply entrenched in the rendering logic that I can't figure out how
# to work around it, and I'm not prepared to uproot the entire thing just so
# I can get this done. So I'm just going to add a little config setting in here
# that will ignore interps to appendices for versions in which those do not exist.
# -JV 2016-01-21

IGNORE_APPENDIX_INTERPS = ['2011-31712', '2012-31311', '2012-3460',
                           '2013-31223', '2014-30404', '2015-26607_20170101',
                           '2015-26607_20180101', '2015-26607_20190101',
                           '2015-26607_20200101', '2015-32285']


def fetch_toc(reg_part, version, flatten=False):
    """Fetch the toc, transform it into a list usable by navigation, etc."""
    api = ApiReader()
    toc = api.layer('toc', reg_part, version)

    toc_list = []
    if reg_part in toc:
        for data in toc[reg_part]:
            if 'Subpart' in data['index']:
                toc_list.append(toc_subpart(data, toc_list, toc))
            elif 'Interp' in data['index']:
                toc_list.append(toc_interp(data, toc_list, toc, version))
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

    if 'label' not in data:
        data['label'] = data['title']

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
    for sub in toc.get('-'.join(data['index']), []):
        element['sub_toc'].append(toc_sect_appendix(sub, so_far))
    return element


def toc_interp(data, so_far, toc, version=None):
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

    reg_part = data['index'][0]
    element['sub_toc'].extend(intro_interps(toc, reg_part))
    element['sub_toc'].extend(subterps(so_far, reg_part, version))
    return element


def intro_interps(toc, reg_part):
    """Logic to fill in any introduction headers for the entire
    interpretations. Note that at some point, we might have headers randomly
    appear elsewhere in the interpretations, unrelated to a specific
    section. That's a @todo."""
    elements = []
    for el in toc.get(reg_part + '-Interp', []):
        if el['index'][1] == 'Interp':
            elements.append({
                'label': 'Interpretations',
                'sub_label': el['title'],
                'index': el['index'],
                'section_id': '-'.join(el['index'])})
    return elements


def subterps(so_far, reg_part, version=None):
    """Logic to build subterps, collections of interpretations for subparts,
    the empty subpart, or appendices"""

    elements = []
    found_subpart = False
    if version in IGNORE_APPENDIX_INTERPS:
        found_appendix = True
    else:
        found_appendix = False

    for el in so_far:
        if el.get('is_subpart'):
            found_subpart = True
            index = el['index'] + ['Interp']
            elements.append({
                'label': el['label'],
                'sub_label': el['sub_label'],
                'index': index,
                'is_subterp': True,
                'section_id': '-'.join(index)
            })
        elif el.get('is_appendix') and not found_appendix:
            found_appendix = True
            index = el['index'][:1] + ['Appendices', 'Interp']
            elements.append({
                'label': 'Appendices',
                'index': index,
                'is_subterp': True,
                'section_id': '-'.join(index)
            })

    if not found_subpart:   # Add the empty subpart
        index = [reg_part, 'Subpart', 'Interp']
        elements.insert(0, {
            'label': 'Regulation Text',
            'index': index,
            'is_subterp': True,
            'section_id': '-'.join(index)
        })
    return elements
