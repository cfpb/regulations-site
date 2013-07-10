import sys
import codecs
from os import mkdir, path
import shutil

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option

from regulations.generator.html_builder import HTMLBuilder
from regulations.generator import generator 
from regulations.generator import notices

class Command(BaseCommand):
    args = "--regulation <regulation part> --reg_version=<regulation version>"
    help = 'Write out the full version of a regulation to disk.'

    option_list = BaseCommand.option_list + (
        make_option('--regulation', 
            action='store',
            dest='regulation_part', 
            help='Regulation required.'), 
        make_option('--reg_version',
            action='store', 
            dest='regulation_version',
            help='Regulation version required.'))

    def write_file(self, filename, markup):
        """ Write out a file using the UTF-8 codec. """
        f = codecs.open(filename, 'w', encoding='utf-8')
        f.write(markup)
        f.close()

    def get_regulation_version(self, **options):
        """ Get the regulation part and regulation version from the command line arguments. """
        regulation_part = options.get('regulation_part')
        regulation_version = options.get('regulation_version')

        if not regulation_part or not regulation_version:
            usage_string = "Usage: python manage.py generate_regulation  %s\n"  % Command.args
            raise CommandError(usage_string)
        return (regulation_part, regulation_version)

    def handle(self, *args, **options):
        regulation_part, regulation_version = self.get_regulation_version(**options)
        inline_applier, p_applier, s_applier = generator.get_all_layers(regulation_part, regulation_version)

        builder = generator.get_builder(regulation_part, regulation_version, 
                inline_applier, p_applier, s_applier)
        builder.generate_html()
        markup = builder.render_markup()

        self.write_file(settings.OFFLINE_OUTPUT_DIR + 'rege.html', markup)
        front_end_dir = settings.OFFLINE_OUTPUT_DIR + '/static/regulations/'

        if not path.islink(front_end_dir):
            if path.exists(front_end_dir):
                shutil.rmtree(front_end_dir)
            shutil.copytree('../regserver/regulations/static/regulations/', front_end_dir)

        if not path.exists(settings.OFFLINE_OUTPUT_DIR + 'notice'):
            mkdir(settings.OFFLINE_OUTPUT_DIR + 'notice')

        all_notices = generator.get_all_notices()
        for notice in all_notices: #notices.fetch_all(api):
            self.write_file(settings.OFFLINE_OUTPUT_DIR + 'notice/' + 
                notice['document_number'] + ".html", notices.markup(notice))
