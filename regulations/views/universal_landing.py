from datetime import datetime

from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import select_template
from regulations.views import utils

from regulations.generator import versions


def filter_future_amendments(versions):
    """ Take a list of amendments, and only return a list of those that 
    are in the future. """
    today = datetime.today()
    amendments = [v for v in versions if v['by_date'] > today]
    amendments.sort(key=lambda v: v['by_date'])
    return amendments


def get_regulations_list(all_versions):
    """ Given a list of regulation versions, add data about those regulations
    to that list. """

    regs = []
    reg_parts = sorted(all_versions.keys())

    for part in reg_parts:
        version = all_versions.get(part)[0]['version']
        reg_meta = utils.regulation_meta(part, version, True)
        first_section = utils.first_section(part, version)
        amendments = filter_future_amendments(all_versions.get(part, None))

        reg = {'part': part,
               'meta': reg_meta,
               'reg_first_section': first_section,
               'amendments': amendments}

        regs.append(reg)
    return regs


def universal(request):
    context = {}
    utils.add_extras(context)

    all_versions = versions.fetch_regulations_and_future_versions()
    regs = get_regulations_list(all_versions)

    context['regulations'] = regs
    context['cfr_title_text'] = regs[0]['meta']['cfr_title_text']
    context['cfr_title_number'] = utils.to_roman(
        regs[0]['meta']['cfr_title_number'])

    c = RequestContext(request, context)
    t = select_template([
        'regulations/universal_landing.html',
        'regulations/generic_universal.html'])
    return HttpResponse(t.render(c))
