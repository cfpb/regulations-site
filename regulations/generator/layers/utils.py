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
