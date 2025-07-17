from django.db import models
class Movie (models.Model):
    NOT_RATED = 'NR',
    RATED_G = 'G',
    RATED_PG = 'PG',
    RATED_R = 'R',
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

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)
