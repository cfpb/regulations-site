from django.template import loader, Context

def fetch_all(api_client):
    """Pull down all known notices from the API"""
    notices = []
    for notice in api_client.notices()['results']:
        notices.append(api_client.notice(notice['document_number']))
    return notices

def markup(notice):
    """Convert a notice's JSON into associated markup"""
    context_dict = dict(notice) #   makes a copy
    sxs_template = loader.get_template('notice-sxs.html')
    context_dict['sxs_markup'] = [sxs_markup(child, 3, sxs_template)
            for child in notice['section_by_section']]

    return loader.get_template('notice.html').render(Context(context_dict))

def sxs_markup(sxs, depth, template):
    """Markup for one node in the sxs tree."""
    context_dict = dict(sxs)    #   makes a copy
    context_dict['depth'] = depth
    context_dict['children'] = [sxs_markup(child, depth+1, template) 
            for child in sxs['children']]
    return template.render(Context(context_dict))
