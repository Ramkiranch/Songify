from django.views import View

from rest_framework.views import APIView

from .models import Song
from .database import DatabaseFunctions
from .result import Result
import json


class SongView(APIView):
    """
    The song view is to create new songs, retrieve the songs by id, name or
    by a match string, delete a song by id
    TODO: Some or most of the logic/validations can be implemented using serializers
    to validate the data
    """

    def get(self, request, *args, **kwargs):
        """
        Return the songs based on the query params id, name or match_string
        If no query params provided, returns list of all songs

        :param request:
        :return: HttpResponse (list of songs or song name)
        """
        match_string = self.request.query_params.get('match_string', None)
        id = self.request.query_params.get('id', None)
        name = self.request.query_params.get('name', None)

        if match_string:
            data = DatabaseFunctions.get_by_match_string(match_string)
            data = json.dumps(data)
        elif id:
            data = DatabaseFunctions.get_by_id(id)
        elif name:
            data = DatabaseFunctions.get_by_name(name)
        else:
            data = DatabaseFunctions.get_all()
            data = json.dumps(data)
        
        return Result.BuildResult(data, 200)
    
    def post(self, request, *args, **kwargs):
        """
        Insert a new song to the favourite list by providing the name,
        artists (in array), album, length of song in seconds in request
        body as json object. The view validates the total songs count
        and total songs length and then inserts into the table, else returns
        error saying too many songs
        :request body example:
        {
	        "name": "Going Bad",
	        "artist": "{Drake, Meek Mill}",
	        "album": "Guide",
	        "length": 300
        }
        :return: HttpResponse new song saved with 201 response
        """
        name = self.request.data.get('name', None)
        artists = self.request.data.get('artist', None)
        album = self.request.data.get('album', None)
        length = self.request.data.get('length', None)

        # Condition to check if empty strings are passed as params
        if artists=="{}" or name=="" or album=="" or length==0:
            raise ValueError("All fields should have values")

        # TODO: we can create a validate function to validate all the params or
        # create validators for the model fields to make sure invalid entries are avoided

        self.total_songs, self.songs_length = self.get_songs_count_length()
        
        current_total_length = self.songs_length + (float(length)/60.0)
        
        # Validates the current songs and length before adding the song
        if self.total_songs > 19 or current_total_length >= 80.0:
            return Result.BuildResult("Songs can't be more than 20 or\
                total songs length should not exceed 80 mins", 400)
        
        new_song = DatabaseFunctions.create(name, artists, album, length)

        if new_song:
            self.total_songs+=1
            self.songs_length+=(float(length)/60.0)
            return Result.BuildResult('New Song saved', 201)
        
        return Result.BuildResult("Song wasn't saved", 400)
    
    def delete(self, request, *args, **kwargs):
        """
        Deletes the songs with query parameter of either id
        or the song name
        :request param id or name:
        :return: HttpResponse
        """
        id = self.request.query_params.get('id', None)
        name = self.request.query_params.get('name', None)

        if id:
            song_to_delete = DatabaseFunctions.get_by_id(id=id)
        if name:
            song_to_delete = DatabaseFunctions.get_by_name(name=name)
        
        self.total_songs, self.songs_length = self.get_songs_count_length()
        ps = DatabaseFunctions.delete(song_to_delete.id)
        
        # Decrement the song count and length after deleting the song
        if ps:
            self.total_songs-=1
            self.songs_length-=(song_to_delete.length/60.0)
            return Result.BuildResult(f'Song {song_to_delete.name} deleted', 200)
        else:
            return Result.BuildResult(f'Song {song_to_delete.name} not deleted', 400)
    
    def get_songs_count_length(self)->tuple:
        """
        Returns the songs count and songs length
        """
        self.total_songs = DatabaseFunctions.get_songs_count()
        self.songs_length = DatabaseFunctions.get_songs_length()

        return (self.total_songs, self.songs_length)

class ArtistView(APIView):
    """
    The artist view retrieves the list of artist(s) of the song.
    """
    def get(self, request, *args, **kwargs):
        """
        Retrieves the list of artist(s) of the the song with query
        params of either id or the song name
        :param request with query param id or name:
        :return: list of artists
        """
        song_name = self.request.query_params.get('song_name', None)
        id = self.request.query_params.get('id', None)

        if song_name:
            artists = DatabaseFunctions.get_artists_by_name(song_name)
        
        if id:
            artists = DatabaseFunctions.get_artists_by_id(id)
        
        if not song_name and not id:
            raise ValueError("Provide either id or the name of the song as query parameter\
                to retrieve the artists of the song")

        return Result.BuildResult(artists, 200)
