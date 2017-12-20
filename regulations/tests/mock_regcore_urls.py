from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.http import Http404, HttpResponseNotFound, JsonResponse


def returns200(request):
    return JsonResponse({'foo': 'bar'})


def returnsGet(request):
    return JsonResponse(request.GET)


def returns404(request):
    return HttpResponseNotFound('not found')


def raisesHttp404(request):
    raise Http404('not found')


def raisesException(request):
    raise RuntimeError('something bad happened')


urlpatterns = [
    url('returns-200', returns200),
    url('returns-get', returnsGet),
    url('returns-404', returns404),
    url('raises-http404', raisesHttp404),
    url('raises-exception', raisesException),
]
