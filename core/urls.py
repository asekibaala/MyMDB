from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('movies', views.MovieListView.as_view(), name='MovieList'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='MovieDetail'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view()),  # <-- Add this line
    #path('404/', views.Custom404View.as_view(), name='Custom404'),
]