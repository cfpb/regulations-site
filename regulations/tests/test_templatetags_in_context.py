from unittest import TestCase

from django.template import Context, Template


class TemplatetagsInContextTest(TestCase):
    def test_in_context(self):
        text = "{% load in_context %}"
        text += "1. {{ f1 }}{{ f2 }}{{ f3 }}{{ f4 }}\n"
        text += "{% begincontext c1 %}\n"
        text += "2. {{ f1 }}{{ f2 }}{{ f3 }}{{ f4 }}\n"
        text += "{% endcontext %}{% begincontext c1 c2 %}\n"
        text += "3. {{ f1 }}{{ f2 }}{{ f3 }}{{ f4 }}\n"
        text += "{% begincontext c2a %}\n"
        text += "4. {{ f1 }}{{ f2 }}{{ f3 }}{{ f4 }}\n"
        text += "{% endcontext %}{% endcontext %}\n"
        text += "5. {{ f1 }}{{ f2 }}{{ f3 }}{{ f4 }}"

        context = {'f1': 'f1',
                   'c1': {'f2': 'c1.f2', 'f1': 'c1.f1'},
                   'c2': {'f2': 'c2.f2',
                          'f3': 'c2.f3', 'c2a': {'f4': 'c2a.f4'}}}

        output = Template(text).render(Context(context))
        lines = output.split("\n")
        self.assertEqual("1. f1", lines[0])
        self.assertEqual("2. c1.f1c1.f2", lines[2])
        self.assertEqual("3. c1.f1c2.f2c2.f3", lines[4])
        self.assertEqual("4. c2a.f4", lines[6])
        self.assertEqual("5. f1", lines[8])

    def test_in_context_cascade(self):
        """Make sure fields that are not dicts get passed along"""
        text = "{% load in_context %}{% begincontext c1 f2 %}"
        text += "{{ f1 }}{{ f2 }}\n"
        text += "{% endcontext %}"
        text += "{{ f1 }}{{ f2 }}"

        context = {'f1': 'f1', 'f2': 'f2', 'c1': {'f1': 'c1.f1'}}
        output = Template(text).render(Context(context))
        lines = output.split("\n")
        self.assertEqual("c1.f1f2", lines[0])
        self.assertEqual("f1f2", lines[1])
