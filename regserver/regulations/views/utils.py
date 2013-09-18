from django.conf import settings
from regulations.generator import generator


def get_layer_list(names):
    layer_names = generator.LayerCreator.LAYERS
    return set(l.lower() for l in names.split(',') if l.lower() in layer_names)


def handle_specified_layers(
        layer_names, regulation_id, version, sectional=False):

    layer_list = get_layer_list(layer_names)
    layer_creator = generator.LayerCreator()
    layer_creator.add_layers(layer_list, regulation_id, version, sectional)
    return layer_creator.get_appliers()

def handle_diff_layers(
    layer_names, regulation_id, older, newer, sectional=False):
    
    layer_list = get_layer_list(layer_names)
    layer_creator = generator.DiffLayerCreator(newer)
    layer_creator.add_layers(layer_list, regulation_id, older, sectional)
    return layer_creator.get_appliers()

def add_extras(context):
    context['env'] = 'source' if settings.DEBUG else 'built'
    context['GOOGLE_ANALYTICS_SITE'] = settings.GOOGLE_ANALYTICS_SITE
    context['GOOGLE_ANALYTICS_ID'] = settings.GOOGLE_ANALYTICS_ID
    return context
