from django.contrib.postgres.fields import ArrayField
from django.db import models

from autoslug import AutoSlugField

class Song(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    slug = AutoSlugField(populate_from='name', always_update=True)
    artist = ArrayField(
        models.CharField(max_length=15), blank=False
        )
    album = models.CharField(max_length=25, blank=False)
    length = models.IntegerField(verbose_name='Length of Song in seconds', blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = verbose_name_plural = 'Favourite Songs'
        ordering = ['id']
        unique_together = ['name', 'album']
    
