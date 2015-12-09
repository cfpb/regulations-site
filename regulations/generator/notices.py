from django.template import loader, Context

from regulations.generator.layers.utils import convert_to_python


def fetch_all(api_client, part):
    """Pull down all known notices from the API"""
    notices = []
    for notice in api_client.notices()['results']:
        notices.append(api_client.notice(notice['document_number']))
    return notices


def get_notice(api_client, part, document_number):
    return api_client.notice(part, document_number)


def markup(notice):
    """Convert a notice's JSON into associated markup"""
    #makes a copy
    context_dict = dict(notice)
    sxs_template = loader.get_template('regulations/notice-sxs.html')
    context_dict['sxs_markup'] = [
        sxs_markup(child, 3, sxs_template)
        for child in notice['section_by_section']]

    return loader.get_template('regulations/notice.html').render(
        Context(context_dict))


def sxs_markup(sxs, depth, template):
    """Markup for one node in the sxs tree."""
    #makes a copy
    context_dict = dict(sxs)
    context_dict['depth'] = depth
    context_dict['children'] = [
        sxs_markup(child, depth+1, template)
        for child in sxs['children']]
    return template.render(Context(context_dict))


def filter_labeled_children(sxs):
    """ Some children don't have labels. We display those with their parents.
    The other children are displayed when they are independently, specifically
    requested. """
    return [s for s in sxs['children'] if 'label' not in s]


def non_empty_sxs(sxs):
    has_paragraphs = len(sxs['paragraphs']) > 0
    has_unlabeled_children = len(filter_labeled_children(sxs)) > 0
    return (has_paragraphs or has_unlabeled_children)


def add_depths(sxs, starting_depth):
    """ We use depth numbers in header tags  to determine how titles are
    output. """

    sxs['depth'] = starting_depth
    for s in sxs['children']:
        add_depths(s, starting_depth+1)


def find_label_in_sxs(sxs_list, label_id, fr_page=None):
    """ Given a tree of SXS sections, find a non-empty sxs that matches
    label_id. Some notices may have the same label appearing multiple times;
    use fr_page to distinguish, defaulting to the first"""

    matches = []

    for s in sxs_list:
        if label_id in s.get('labels', [s.get('label')]) and non_empty_sxs(s):
            matches.append(s)
        elif s['children']:
            sxs = find_label_in_sxs(s['children'], label_id, fr_page)
            if sxs and non_empty_sxs(sxs):
                matches.append(sxs)

    perfect_match = [m for m in matches if m.get('page') == fr_page]
    if perfect_match:
        return perfect_match[0]
    if matches:
        return matches[0]
