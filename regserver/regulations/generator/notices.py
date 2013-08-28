from datetime import datetime
from django.template import loader, Context


def fetch_all(api_client):
    """Pull down all known notices from the API"""
    notices = []
    for notice in api_client.notices()['results']:
        notices.append(api_client.notice(notice['document_number']))
    return notices


def get_notice(api_client, document_number):
    return api_client.notice(document_number)


def markup(notice):
    """Convert a notice's JSON into associated markup"""
    #makes a copy
    context_dict = dict(notice)
    sxs_template = loader.get_template('notice-sxs.html')
    context_dict['sxs_markup'] = [
        sxs_markup(child, 3, sxs_template)
        for child in notice['section_by_section']]

    return loader.get_template('notice.html').render(Context(context_dict))


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


def extract_notice_metadata(notice):
    """ From a notice, extract the data that we're interested in
    displaying for the section by section analysis. """

    data_list = [
        'action', 'document_number', 'fr_url', 'publication_date',
        'effective_on', 'regulation_id_numbers']

    metadata = {}
    for d in data_list:
        metadata[d] = notice[d]

    metadata['effective_on'] = datetime.strptime(
        metadata['effective_on'], "%Y-%m-%d")

    metadata['publication_date'] = datetime.strptime(
        metadata['publication_date'], "%Y-%m-%d")

    return metadata


def find_label_in_sxs(sxs_list, label_id):
    """ Given a tree of SXS sections, find a non-empty sxs that matches
    label_id. """

    for s in sxs_list:
        if 'label' in s:
            if s['label'] == label_id:
                if non_empty_sxs(s):
                    return s
            elif s['children'] and label_id.startswith(s['label']):
                sxs = find_label_in_sxs(s['children'], label_id)
                if sxs and non_empty_sxs(sxs):
                    return sxs
