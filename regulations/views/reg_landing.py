from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import select_template

from regulations.generator import api_reader
from regulations.generator.versions import fetch_grouped_history
from regulations.views import utils


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
        if current:
            current_version = current[0]
        else:
            current_version = next_version
        return (current_version, next_version)


def regulation(request, label_id):

    context = {}
    current_version, new_version = get_versions(label_id)
    if new_version:
        context['new_version'] = new_version
    context['current_version'] = current_version

    context['label_id'] = label_id
    context['reg_first_section'] = utils.first_section(
        label_id, current_version['version'])
    context['reg_part'] = label_id.split('-')[0]

    regulation_meta = utils.regulation_meta(
        label_id,
        current_version['version'],
        True)
    context['meta'] = regulation_meta


    c = RequestContext(request, context)

    t = select_template([
        'regulations/specific/landing_%s.html' % label_id,
        'regulations/landing_base.html',
        'regulations/generic_landing.html'])
    return HttpResponse(t.render(c))
