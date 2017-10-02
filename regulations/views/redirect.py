from datetime import date
import re

from django.shortcuts import redirect

from regulations.generator.api_reader import ApiReader
from regulations.generator.versions import fetch_grouped_history
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
        return redirect('chrome_interp_view', label_id, last_version)
    elif last_version and len(label_parts) == 1:
        return redirect('chrome_regulation_view', label_id, last_version)
    elif last_version:
        return redirect('chrome_paragraph_view', label_id, last_version)
    else:
        return handle_generic_404(request)


def redirect_by_date_get(request, label_id):
    """Handles date, etc. if they are part of the GET variable. We check for
    bad data here (as we can't rely on url regex)"""
    try:
        year = abs(int(request.GET.get('year')))
        month = abs(int(request.GET.get('month')))
        day = abs(int(request.GET.get('day')))

        if year < 100:  # Assume two-digit years are for 2000
            year = 2000 + year

        return redirect_by_date(request, label_id, "%04d" % year,
                                "%02d" % month, "%02d" % day)
    except (ValueError, TypeError):
        return handle_generic_404(request)


def order_diff_versions(label_id, version, new_version):
    # Re-order if needed - History is sorted in reverse chronological order
    for major_version in fetch_grouped_history(label_id.split('-')[0]):
        for notice in major_version['notices']:
            # Hit the "old" version first, meaning it's not actually the old
            # version
            if notice['document_number'] == version:
                return redirect('chrome_section_diff_view', label_id,
                                new_version, version)
            # Hit the new version first -- sort is correct
            elif notice['document_number'] == new_version:
                return redirect('chrome_section_diff_view', label_id,
                                version, new_version)

    # Didn't find the versions in question. Assume this was intentional
    return redirect('chrome_section_diff_view', label_id, version,
                    new_version)


def diff_redirect(request, label_id, version):
    """Handles constructing the diff url by pulling the new version from
    GET. We check for bad data here (as we can't rely on url regex)"""
    new_version = request.GET.get('new_version', '')
    if not re.match(r'^[-\d\w]+$', new_version):
        return handle_generic_404(request)

    response = order_diff_versions(label_id, version, new_version)
    response['Location'] += '?from_version=%s' % version
    return response
