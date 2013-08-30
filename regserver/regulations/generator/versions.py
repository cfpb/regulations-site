from datetime import datetime

from django.conf import settings

from regulations.generator import api_reader
from regulations.generator.layers.utils import convert_to_python


def fetch_grouped_history(part):
    client = api_reader.ApiReader()
    versions = filter(lambda v: 'by_date' in v,
                      client.regversions(part)['versions'])
    for version in versions:
        version['notices'] = []
    versions = sorted(convert_to_python(versions), reverse=True,
                      key=lambda v: v['by_date'])

    today = datetime.today()
    seen_current = False

    for version in versions:
        if version['by_date'] > today:
            version['timeline'] = 'future'
        elif not seen_current:
            seen_current = True
            version['timeline'] = 'current'
        else:
            version['timeline'] = 'past'

    for notice in client.notices(part)['results']:
        notice = convert_to_python(notice)
        for v in (v for v in versions
                  if v['by_date'] == notice['effective_on']):
            v['notices'].append(notice)

    for version in versions:
        version['notices'] = sorted(version['notices'], reverse=True,
                                    key=lambda n: n['publication_date'])

    return versions
