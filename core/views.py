from django.views.generic import (ListView, DetailView)
from core.models import Movie,Person, Vote,VoteManager
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from core.forms import VoteForm
from django.views.generic import CreateView, UpdateView 
from django.urls import reverse

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
    
class MovieListView(ListView):
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
