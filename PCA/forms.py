from django import forms
from . import models

class CreateWord(forms.ModelForm):
    class Meta:
        model  = models.Word
        fields = ['word', 'difficulty']


