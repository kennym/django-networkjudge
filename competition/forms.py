from django import forms

from competition.models import (
    Submission
)

class UploadSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('language', 'source_code',)

class EvaluateSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('accepted', 'ignored',)
