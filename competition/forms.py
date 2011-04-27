from django import forms

from competition.models import (
    Solution,
)

class UploadSolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ('language', 'source_code',)
