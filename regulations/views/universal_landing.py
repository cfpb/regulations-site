from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import select_template
from regulations.views import utils

def universal(request):
   context = {} 
   utils.add_extras(context)
   c = RequestContext(request, context)
   t = select_template([
        'regulations/universal_landing.html',
        'regulations/generic_universal.html'])
   return HttpResponse(t.render(c))