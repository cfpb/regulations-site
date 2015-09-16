from django import template

register = template.Library()


class InContextNode(template.Node):
    def __init__(self, nodelist, subcontext_names):
        self.nodelist = nodelist
        self.subcontext_names = subcontext_names

    def render(self, context):
        new_context = {}
        for field in self.subcontext_names:
            value = context.get(field, {})
            if isinstance(value, dict):
                new_context.update(context.get(field, {}))
            else:
                new_context[field] = value
        new_context = context.new(new_context)
        return self.nodelist.render(new_context)


@register.tag('begincontext')
def in_context(parser, token):
    """
    Replaces the context (inside of this block) for easy (and safe) inclusion
    of sub-content.

    For example, if the context is {'name': 'Kitty', 'sub': {'size': 5}}

        1: {{ name }} {{ size }}
        {% begincontext sub %}
        2: {{ name }} {{ size }}
        {% endcontext %}
        3: {{ name }} {{ size }}

    Will print
        1: Kitty
        2:  5
        3: Kitty

    Arguments which are not dictionaries will 'cascade' into the inner
    context.
    """
    nodelist = parser.parse(('endcontext',))
    parser.delete_first_token()
    return InContextNode(nodelist, token.split_contents()[1:])
