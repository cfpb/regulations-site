import sys
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from regulations.generator.html_builder import HTMLBuilder
from regulations.generator.generator import get_all_layers

class Command(BaseCommand):
    args = "--regulation <regulation part> --reg_version=<regulation version>"
    help = 'LabelCommand related stuff'

    option_list = BaseCommand.option_list + (
        make_option('--regulation', 
            action='store',
            dest='regulation_part', 
            help='Regulation required.'), 
        make_option('--reg_version',
            action='store', 
            dest='regulation_version',
            help='Regulation version required.'))

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
        inline_applier, p_applier, s_applier = get_all_layers(regulation_part, regulation_version)
