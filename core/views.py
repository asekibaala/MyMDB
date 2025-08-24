from django.views.generic import (ListView, DetailView)
from core.models import Movie

class MovieDetailView(DetailView):
    #model = Movie
    queryset = Movie.objects.all_with_related_persons()

class MovieListView(ListView):
    model = Movie
    paginate_by = 10

class PersonDetailView(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()
