# filepath: /Users/asekibaala/Documents/MyMDB/core/forms.py
from django import forms
from .models import Vote

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['value']  # or whatever fields your Vote model has