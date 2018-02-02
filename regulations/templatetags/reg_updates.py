from django import template
from django.conf import settings


register = template.Library()


@register.assignment_tag
def update_in_progress(label_id):
    """Given a regulation, is there an update currently in progress?

    This template tag checks for a list in the Django setting
    EREGS_REGULATION_UPDATES, and, if that setting exists, checks if the given
    regulation part is in that list.

    Use it in a template like:

        {% update_in_progress label_id as reg_update_in_progress %}
        {% if reg_update_in_progress %}
        <p>An update is in progress to this regulation.</p>
        {% endif %}
    """
    regulation_updates = getattr(settings, 'EREGS_REGULATION_UPDATES', [])
    reg_part = label_id.split('-')[0]
    return reg_part in regulation_updates
