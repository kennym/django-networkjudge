from django import forms

from competition.models import (
    Submission
)

class UploadSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('language', 'source_code',)

class VerifySubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('verified',)

class IgnoreSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('ignored',)
