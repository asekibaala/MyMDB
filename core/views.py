from django.shortcuts import render
from django.views.generic import ListView
from core.models import Movie

class MovieListView(ListView):
    model = Movie
  
