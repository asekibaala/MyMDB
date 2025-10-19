from django.views.generic import (ListView, DetailView)
from core.models import Movie,Person, Vote,VoteManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import MovieImageForm, VoteForm
from django.views.generic import CreateView, UpdateView 
from django.urls import reverse
from core.mixins import CachePageVaryOnCookiesMixin
import django
from django.core.cache import caches

class MovieDetailView(DetailView):
    #model = Movie
    queryset = Movie.objects.all_with_related_persons_and_score()
    #queryset = Movie.objects.all_with_related_persons()
    #queryset = Movie.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object,
                user=self.request.user
            )
            if vote.id:
                vote_form_url = reverse('core:UpdateVote', kwargs={'movie_id': self.object.id, 'pk': vote.id})
            else:
                vote_form_url = reverse('core:CreateVote',kwargs={'movie_id':self.object.id})
            vote_form = VoteForm(instance=vote)
            context['vote_form'] = vote_form
            context['vote_form_url'] = vote_form_url
        return context

    def movie_image_form(self):
        if self.request.user.is_authenticated:
            return MovieImageForm()
        return None
class MovieListView(CachePageVaryOnCookiesMixin, ListView):
    model = Movie
    paginate_by = 10

class PersonDetailView(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()

class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm
    def get_initial(self):
        initial = super().get_initial()
        initial['movie'] = Movie.objects.get(id=self.kwargs['movie_id'])
        initial['user'] = self.request.user
        return initial
    def get_success_url(self):
        movie_id = self.kwargs['movie_id']
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})
    
    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(movie_detail_url)
    
class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset = None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied("You cannot edit someone else's vote.")
        return vote
    def get_success_url(self):
        movie_id = self.kwargs['movie_id']
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})
    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(movie_detail_url)
class MovieImageUploadView(LoginRequiredMixin, CreateView):
    form_class = MovieImageForm

    def get_initial(self):
        initial = super().get_initial()
        initial['movie'] = Movie.objects.get(id=self.kwargs['movie_id'])
        initial['user'] = self.request.user
        return initial
    def render_to_response(self, context, **response_kwargs):
        movie_id  = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)

    def get_success_url(self):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return movie_detail_url
    
class TopMoviesView(ListView):  
    template_name = 'core/top_movies_list.html'
    queryset = Movie.objects.top_movies(limit=10)

    def get_queryset(self):
        limit = 10
        key = 'top_movies_{}'.format(limit)
        cached_qs = caches['default'].get(key)
        if cached_qs:
            same_django = cached_qs._django_version == django.get_version()
            if same_django:
                return cached_qs
        qs = Movie.objects.top_movies(limit=limit)  
        caches['default'].set(key, qs, timeout=300)
        return qs