#!/usr/bin/env python

import codecs
import json

from layers.external_citation import ExternalCitationLayer
from layers.internal_citation import InternalCitationLayer
from layers.definitions import DefinitionsLayer
from layers.layers_applier import LayersApplier
from layers.toc_applier import TableOfContentsLayer
from html_builder import HTMLBuilder
import api_stub

from django.conf import settings

def write_file(filename, markup):
    """ Write out a file using the UTF-8 codec. """
    f = codecs.open(filename, 'w', encoding='utf-8')
    f.write(markup)
    f.close()

if __name__ == "__main__":
    if not settings.configured:
        settings.configure(TEMPLATE_DEBUG=False, 
            TEMPLATE_LOADERS=('django.template.loaders.filesystem.Loader',), 
            TEMPLATE_DIRS = ('templates/',))

    reg_json = api_stub.get_regulation_as_json('regulations/rege/rege.json')

    layers_applier = LayersApplier()

    el = json.load(open('regulations/rege/external_citations_layer.json'))
    reference_EFT_act = ['15', '1693'] #Title 15, Section 1693 of the United States Code

    layers_applier.add_layer(ExternalCitationLayer(el, ['15', '1693']))
    il = json.load(open('regulations/rege/internal_citations_layer.json'))
    layers_applier.add_layer(InternalCitationLayer(il))

    dl = json.load(open('regulations/rege/terms.json'))
    layers_applier.add_layer(DefinitionsLayer(dl))

    tl = json.load(open('regulations/rege/toc_layer.json'))
    toc_applier = TableOfContentsLayer(tl)
    
    makers_markup = HTMLBuilder(layers_applier, toc_applier)
    makers_markup.tree = reg_json
    makers_markup.generate_html()
    markup = makers_markup.render_markup()

    write_file('/tmp/rege.html', markup)
