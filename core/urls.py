from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('movies', views.MovieListView.as_view(), name='MovieList'),
    # Add more URL patterns as needed
]