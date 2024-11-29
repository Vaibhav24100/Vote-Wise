from django import forms
from .models import VotingForm, Question, Option

class CreateVotingForm(forms.ModelForm):
    class Meta:
        model = VotingForm
        fields = []

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text']
