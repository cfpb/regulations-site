from django import template

register = template.Library()

@register.filter
def format_marker(marker_string):
    marker = marker_string.replace('(', '')
    marker = marker.replace(')', '')
    marker = marker.replace('.', '')

    return marker