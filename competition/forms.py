from django.utils.translation import ugettext_lazy as _, ugettext
from django import forms

from competition.models import Solution

class UploadSolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        exclude = ('participant', 'problem',)
