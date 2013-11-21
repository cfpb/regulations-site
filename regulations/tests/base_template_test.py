from unittest import TestCase
from django.template import RequestContext
from django.template.loader import get_template
from django.test import RequestFactory


class TemplateTest(TestCase):
    def test_title_in_base(self):
        context = {
            'env': 'dev',
            'reg_part': '204',
            'meta': {'reg_letter': 'F', 'statutory_name': 'My Reg'}}
        request = RequestFactory().get('/fake-path')
        c = RequestContext(request, context)
        t = get_template('regulations/base.html')
        rendered = t.render(c)

        title = 'PART 204 - MY REG (REGULATION F)'
        self.assertTrue(title in rendered)
