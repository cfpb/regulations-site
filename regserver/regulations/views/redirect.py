from datetime import date

from django.shortcuts import redirect

from regulations.generator.api_reader import ApiReader
from regulations.views.error_handling import handle_generic_404


def redirect_by_date(request, label_id, year, month, day):
    """If a user requests a date as the version, find the version which was
    current as of that date"""
    date_versions = []
    client = ApiReader()
    for struct in client.regversions(label_id.split('-')[0])['versions']:
        if 'by_date' in struct:
            date_versions.append((struct['by_date'], struct['version']))

    date_versions = sorted(date_versions)
    last_version = None
    date_str = '%s-%s-%s' % (year, month, day)
    while date_versions and date_versions[0][0] <= date_str:
        last_version = date_versions[0][1]
        date_versions = date_versions[1:]

    label_parts = label_id.split('-')
    if last_version and len(label_parts) == 2:
        return redirect('chrome_section_view', label_id, last_version)
    elif last_version and label_parts[-1] == 'Interp':
        return redirect('chrome_section_view', label_id, last_version)
    elif last_version and len(label_parts) == 1:
        return redirect('chrome_regulation_view', label_id, last_version)
    elif last_version:
        return redirect('chrome_paragraph_view', label_id, last_version)
    else:
        return handle_generic_404(request)


def redirect_by_date_get(request, label_id):
    """Handles date, etc. if they are part of the GET variable"""
    return redirect_by_date(request, label_id, request.GET.get('year'),
                            request.GET.get('month'), request.GET.get('day'))
