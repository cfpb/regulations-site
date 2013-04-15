from layers.external_citation import ExternalCitationLayer
from layers.internal_citation import InternalCitationLayer
from layers.layers_applier import LayersApplier
from html_builder import HTMLBuilder

if __name__ == "__main__":
    reg_json = api_stub.get_regulation_as_json('/vagrant/data/regulations/rege/rege.json')

    layers_applier = LayersApplier()

    el = json.load(open('regulations/rege/external_citations_layer.json'))
    layers_applier.add_layer(ExternalCitationLayer(el))
    il = json.load(open('regulations/rege/internal_citations_layer.json'))
    layers_applier.add_layer(InternalCitationLayer(il))
    
    makers_markup = HTMLBuilder(layers_applier)
    makers_markup.tree = reg_json
    makers_markup.generate_html()
    markup = makers_markup.render_markup()

    write_file('/tmp/rege.html', markup)
