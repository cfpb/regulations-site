from datetime import datetime
import re

from django.template import Context
from django.core import cache
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import Context

from regulations.generator.node_types import to_markup_id


def convert_to_python(data):
    """Convert raw data (e.g. from json conversion) into the appropriate
    Python objects"""
    if isinstance(data, str) or isinstance(data, unicode):
        #   Dates
        if re.match(r'^\d{4}-\d{2}-\d{2}$', data):
            return datetime.strptime(data, '%Y-%m-%d')
    if isinstance(data, dict):
        new_data = {}
        for key in data:
            new_data[key] = convert_to_python(data[key])
        return new_data
    if isinstance(data, tuple):
        return tuple(map(convert_to_python, data))
    if isinstance(data, list):
        return list(map(convert_to_python, data))
    
    return data


def render_template(template, context):
    c = Context(context)
    return template.render(c).strip('\n')


class RegUrl(object):
    def __init__(self):
        self.cache = {}

    @staticmethod
    def of(citation, version, sectional):
        url = ''

        view_name = 'chrome_section_view'
        # Subterps, collections of interpretations of whole subparts, etc.
        if 'Interp' in citation and ('Subpart' in citation 
                                     or 'Appendices' in citation):
            view_name = 'chrome_subterp_view'
            label = '-'.join(citation)
        elif 'Interp' in citation:
            label = citation[0] + '-Interp'
        else:
            label = '-'.join(citation[:2])

        if sectional:
            try:
                url = reverse(view_name, args=(label, version))
            except NoReverseMatch:
                #XXX We have some errors in our layers. Once those are fixed, we
                #need to revisit this.
                pass
        return url + '#' + '-'.join(to_markup_id(citation))

    def fetch(self, citation, version, sectional):
        key = (tuple(citation), version, sectional)
        if key not in self.cache:
            self.cache[key] = RegUrl.of(citation, version, sectional)
        return self.cache[key]
