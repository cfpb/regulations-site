from regulations.generator import generator

def get_layer_list(names):
    return set(l.lower() for l in names.split(',') if l.lower() in generator.LayerCreator.LAYERS)

def handle_specified_layers(layer_names, regulation_id, version, sectional=False):

    layer_list = get_layer_list(layer_names)
    layer_creator = generator.LayerCreator()
    layer_creator.add_layers(layer_list, regulation_id, version, sectional)
    return layer_creator.get_appliers()
