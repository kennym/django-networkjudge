from django import forms

from competition.models import (
    Submission,
    Competition
)

class StartCompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ('duration',)

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
