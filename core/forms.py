# filepath: /Users/asekibaala/Documents/MyMDB/core/forms.py
from django import forms
from core.models import MovieImage
from django.contrib.auth import get_user_model
from core.models import Vote
from core.models import Movie


class MovieImageForm(forms.ModelForm):
    movie = forms.ModelChoiceField(
        widget=forms.HiddenInput(),
        queryset=Movie.objects.all()
        disabled=True
    )
    user = forms.ModelChoiceField(  
        widget=forms.HiddenInput(),
        queryset=get_user_model().objects.all(),
        disabled=True
    )
    class Meta:
        model = MovieImage
        fields = ['movie', 'user', 'image']
        