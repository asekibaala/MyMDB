from django.db import models
from django.conf import settings
from django.db.models.aggregates import sum
from uuid import uuid4

#from core.models import MovieManager
class PersonManager(models.Manager):
    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related(
            'directed',
            'writing_credits',
            'acting_credits__movie'
        )

class MovieManager(models.Manager):
    def all_with_related_persons(self):
        qs = self.get_queryset()
        return qs.select_related('director').prefetch_related('writers', 'actors')
    def all_with_related_persons_and_score(self):
        qs = self.all_with_related_persons()
        qs = qs.annotate(score=sum('vote__value'))
        return qs
    
class Movie (models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED,'NR - Not Rated'),
        (RATED_G,'G - General Audiences'),
        (RATED_PG,'PG - Parental Guidance'),
        (RATED_R,'R - Restricted'),)
    
    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveBigIntegerField() 
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)

    objects = MovieManager()

    

    class Meta:
        ordering = ['-year', 'title']
    
    

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)

    director = models.ForeignKey(to='Person', 
                                 on_delete=models.SET_NULL, 
                                 null=True,
                                 blank=True,
                                 related_name='directed')
    writers = models.ManyToManyField(to='Person', 
                                     blank=True, 
                                     related_name='writing_credits')
    actors = models.ManyToManyField(to='Person',
                                    through='Role',
                                    blank=True,
                                    related_name='acting_credits')
    
class Role(models.Model):
    movie = models.ForeignKey(to='Movie', on_delete=models.DO_NOTHING)
    person = models.ForeignKey(to='Person', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=140)

    def __str__(self):
        return "{} {} {}".format(self.movie_id, self.person_id, self.name)

class Person(models.Model):
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    born = models.DateField()
    died = models.DateField(blank=True, null=True)

    objects = PersonManager()

    class Meta:
        ordering = ['last_name', 'first_name']
        

    def __str__(self):
        if self.died:
            return '{}, {} ({}-{})'.format(self.last_name, self.first_name, self.born.year, self.died.year)
        return '{}, {} ({})'.format(self.last_name, self.first_name, self.born.year)




class VoteManager(models.Manager):
    def get_vote_or_unsaved_blank_vote(self,movie,user):
        try:
            return Vote.objects.get(
                movie=movie,
                user = user
            )
        except Vote.DoesNotExist:
            return Vote(
                movie=movie,
                user=user
            )
class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
        (UP, 'Upvote'),
        (DOWN, 'Downvote'),
    )

    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now_add=True)

    objects = VoteManager()
    class Meta:
        unique_together = ('user', 'movie')

def movie_directory_path_with_uuid(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return f'uploaded/movies/{instance.movie.id}/{filename}'

class MovieImage(models.Model):
    image = models.ImageField(upload_to=movie_directory_path_with_uuid)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='images')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)