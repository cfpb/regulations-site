import codecs
from os import mkdir, path
import shutil

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.http import HttpRequest
from django.template import Context, loader
from optparse import make_option

from regulations.generator import generator 
from regulations.generator import notices
from regulations.views.chrome import ChromeRegulationView

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
        part, version = self.get_regulation_version(**options)

        view = ChromeRegulationView()
        view.request = HttpRequest()
        view.request.method = 'GET'
        context = view.get_context_data(label_id=part, version=version)
        template = loader.get_template(ChromeRegulationView.template_name)
        markup = template.render(Context(context))

       # markup = builder.render_markup()

        self.write_file(settings.OFFLINE_OUTPUT_DIR + 'rege.html', markup)
        front_end_dir = settings.OFFLINE_OUTPUT_DIR + 'static'

        #   If any dir in the path is symlinked, don't replace it
        if not path.islink(front_end_dir):
            #   Otherwise, copy the static dir to the output
            if path.exists(front_end_dir):
                shutil.rmtree(front_end_dir)
            shutil.copytree('../regulations/static/', front_end_dir)

        if not path.exists(settings.OFFLINE_OUTPUT_DIR + 'notice'):
            mkdir(settings.OFFLINE_OUTPUT_DIR + 'notice')

        all_notices = generator.get_all_notices(options.get('regulation_part'))
        for notice in all_notices: #notices.fetch_all(api):
            self.write_file(settings.OFFLINE_OUTPUT_DIR + 'notice/' + 
                notice['document_number'] + ".html", notices.markup(notice))
