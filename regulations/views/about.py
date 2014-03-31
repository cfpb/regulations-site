from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import select_template
from regulations.views import utils

def about(request):
   context = {} 
   utils.add_extras(context)
   c = RequestContext(request, context)
   t = select_template([
        'regulations/custom-about.html',
        'regulations/about.html'])
   return HttpResponse(t.render(c))
