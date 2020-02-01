from django.contrib import admin
from django.db import models

from .models import Song

class SongAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug": ("name",)}
    model = Song
    list_display = ('id', 'name', 'slug', 'artist', 'album', 'length',)

admin.site.register(Song, SongAdmin)
