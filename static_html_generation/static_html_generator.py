#!/usr/bin/env python

import codecs
import json
from os import path
import shutil

from layers.external_citation import ExternalCitationLayer
from layers.internal_citation import InternalCitationLayer
from layers.definitions import DefinitionsLayer
from layers.layers_applier import LayersApplier
from layers.toc_applier import TableOfContentsLayer
from html_builder import HTMLBuilder
import api_reader

import settings as app_settings
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

    api = api_reader.Client(app_settings.API_BASE)
    regulation, version = "1005", "20111227"
    reg_json = api.regulation(regulation, version)

    layers_applier = LayersApplier()

    el = api.layer("external-citations", regulation, version)
    reference_EFT_act = ['15', '1693'] #Title 15, Section 1693 of the United States Code

    layers_applier.add_layer(ExternalCitationLayer(el, ['15', '1693']))
    il = api.layer("internal-citations", regulation, version)
    layers_applier.add_layer(InternalCitationLayer(il))

    dl = api.layer("terms", regulation, version)
    layers_applier.add_layer(DefinitionsLayer(dl))

    tl = api.layer("toc", regulation, version)
    toc_applier = TableOfContentsLayer(tl)
    
    makers_markup = HTMLBuilder(layers_applier, toc_applier)
    makers_markup.tree = reg_json
    makers_markup.generate_html()
    markup = makers_markup.render_markup()

    write_file('/tmp/rege.html', markup)
    if not path.exists('/tmp/static'):
        shutil.copytree('../static/', '/tmp/static', True)
