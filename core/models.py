from django.db import models
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

    class Meta:
        ordering = ['-year', 'title']
    
    

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)

class Person(models.Model):
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    born = models.DateField()
    died = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        

    def __str__(self):
        if self.died:
            return '{}, {} ({}-{})'.format(self.last_name, self.first_name, self.born.year, self.died.year)
        return '{}, {} ({})'.format(self.last_name, self.first_name, self.born.year)
