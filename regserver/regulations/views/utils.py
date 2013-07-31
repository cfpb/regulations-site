from regulations.generator import generator

def handle_specified_layers(layer_names, regulation_id, version, sectional=False):
    layer_list = [l.lower() for l in layer_names.split(',')]

    layer_creator = generator.LayerCreator()
    layer_creator.add_layers(layer_list, regulation_id, version, sectional)
    return layer_creator.get_appliers()
