from django.core.management.base import BaseCommand
from eregs_cache import EregsCache
import sys


class Command(BaseCommand):
    args = "<url where eregulations is located> <optional- comma seperated list of regulation locations to be parsed >"
    help = 'call every page in eregulations allowing the pages to be cached'

    def handle(self, *args, **options):

        regulations_arg = None
        if len(sys.argv) > 3:
            regulations_arg = sys.argv[3]
    
        EregsCache(sys.argv[2], regulations_arg)
