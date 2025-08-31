from django.db import models
#from core.models import MovieManager
class MovieManager(models.Manager):
    pass
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