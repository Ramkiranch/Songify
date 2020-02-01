from django.contrib import admin
from django.urls import path

from .views import SongView, ArtistView

app_name = 'songify'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('song/name/', SongView.as_view(), name='songs-name'),
    path('song/artist/', ArtistView.as_view(), name='artists-name'),
]
