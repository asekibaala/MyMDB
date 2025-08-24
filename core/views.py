from django.views.generic import (ListView, DetailView)
from core.models import Movie

class MovieDetailView(DetailView):
    model = Movie

class MovieListView(ListView):
    model = Movie
    paginate_by = 10
