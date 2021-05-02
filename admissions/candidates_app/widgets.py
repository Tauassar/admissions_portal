from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class FileWidget(forms.FileInput):
    """
    A FileField Widget that shows its current value if it has one.
    """

    def __init__(self, attrs={}):
        super(FileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and hasattr(value, "url"):
            output.append('<a target="_blank" href="%s">Current file</a>%s ' % \
                          (value.url, _('Change:')))
        output.append(super(FileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
