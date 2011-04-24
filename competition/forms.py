from django import forms

from competition.models import Solution

class UploadSolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        exclude = ('participant', 'problem', 'result', 'submit_time', 'error_message')
