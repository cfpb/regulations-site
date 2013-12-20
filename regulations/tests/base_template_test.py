from unittest import TestCase
from django.template import RequestContext
from django.template.loader import get_template
from django.test import RequestFactory


class TemplateTest(TestCase):
    def test_title_in_base(self):
        context = {
            'env': 'dev',
            'reg_part': '204',
            'meta': {'cfr_title_number': '2'}}
        request = RequestFactory().get('/fake-path')
        c = RequestContext(request, context)
        t = get_template('regulations/base.html')
        rendered = t.render(c)

        title = '2 CFR Part 204 | eRegulations'
        self.assertTrue(title in rendered)
