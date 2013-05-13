#!/usr/bin/env python

import codecs
import json
from os import mkdir, path
import shutil

import api_reader
from layers.analyses import SectionBySectionLayer
from layers.external_citation import ExternalCitationLayer
from layers.internal_citation import InternalCitationLayer
from layers.definitions import DefinitionsLayer
from layers.interpretations import InterpretationsLayer
from layers.layers_applier import LayersApplier
from layers.toc_applier import TableOfContentsLayer
import notices
from html_builder import HTMLBuilder

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
    regulation, version = "1005", "2011-31725"
    reg_json = api.regulation(regulation, version)

    layers_applier = LayersApplier()

    el = api.layer("external-citations", regulation, version)
    reference_EFT_act = ['15', '1693'] #Title 15, Section 1693 of the United States Code

    layers_applier.add_layer(ExternalCitationLayer(el, ['15', '1693']))
    il = api.layer("internal-citations", regulation, version)
    layers_applier.add_layer(InternalCitationLayer(il))

    dl = api.layer("terms", regulation, version)
    layers_applier.add_layer(DefinitionsLayer(dl))

    intl = api.layer("interpretations", regulation, version)
    layers_applier.add_layer(InterpretationsLayer(intl))
    
    sxs = api.layer("analyses", regulation, version)
    layers_applier.add_layer(SectionBySectionLayer(sxs))
    
    tl = api.layer("toc", regulation, version)
    toc_applier = TableOfContentsLayer(tl)

    makers_markup = HTMLBuilder(layers_applier, toc_applier)
    makers_markup.tree = reg_json
    makers_markup.generate_html()
    markup = makers_markup.render_markup()

    write_file('/tmp/rege.html', markup)
    front_end_dir = '/tmp/front_end'
    if not path.islink(front_end_dir):
        if path.exists(front_end_dir):
            shutil.rmtree(front_end_dir)
        shutil.copytree('../front_end', front_end_dir)

    if not path.exists('/tmp/notice'):
        mkdir('/tmp/notice')
    for notice in notices.fetch_all(api):
        write_file('/tmp/notice/' + notice['document_number'] + ".html",
                notices.markup(notice))
