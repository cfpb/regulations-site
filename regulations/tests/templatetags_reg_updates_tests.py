from django.conf import settings
from django.template import Context, Template
from django.test import SimpleTestCase, override_settings


class RegUpdatesTemplateTagsTestCase(SimpleTestCase):
    def render(self, label_id):
        template = Template(
            "{% load reg_updates %}"
            "{% update_in_progress label_id as reg_update %}"
            "{{ reg_update }}"
        )
        context = Context({'label_id': label_id})
        return template.render(context)

    @override_settings()
    def test_no_setting_reg_not_being_updated_returns_false(self):
        del settings.EREGS_REGULATION_UPDATES
        self.assertEqual(self.render('1099-1'), 'False')

    @override_settings(EREGS_REGULATION_UPDATES=['1098', '1099'])
    def test_setting_includes_reg_returns_true(self):
        self.assertEqual(self.render('1099-1'), 'True')

    @override_settings(EREGS_REGULATION_UPDATES=['1001', '1002'])
    def test_setting_doesnt_include_reg_returns_false(self):
        self.assertEqual(self.render('1099-1'), 'False')
