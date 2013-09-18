from django.http import HttpResponse
from django.http import Http404
from django.template import RequestContext
from django.template.loader import select_template

from regulations.generator import api_reader
from regulations.generator.versions import fetch_grouped_history


def regulation_exists(label_id):
    client = api_reader.ApiReader()
    vr = client.regversions(label_id)
    return (vr and len(vr) > 0)


def get_versions(label_id):
    """ Get the current and next version of the regulation. """
    history = fetch_grouped_history(label_id)
    if history:
        future = [h for h in history if h['timeline'] == 'future']
        if len(future) > 0:
            next_version = future[-1]
        else:
            next_version = None

        current = [h for h in history if h['timeline'] == 'current']
        current_version = current[0]
        return (current_version, next_version)


def first_section(label_id):
    """ Return a label to the first section of a regulation. """
    return '%s-1' % label_id


def regulation(request, label_id):

    if not regulation_exists(label_id):
        raise Http404

    context = {}
    current_version, new_version = get_versions(label_id)
    if new_version:
        context['new_version'] = new_version
    context['current_version'] = current_version

    context['label_id'] = label_id
    context['reg_first_section'] = first_section(label_id)

    c = RequestContext(request, context)

    t = select_template([
        'landing_%s.html' % label_id,
        'generic_landing.html'])
    return HttpResponse(t.render(c))
