from django.db.models import Sum
from django.db.utils import DataError
from django.core.exceptions import ObjectDoesNotExist

from .models import Song
from .result import Result

class DatabaseFunctions:
    """
    Database functions to retrieve the list of songs based on id, name or
    match string, create new favourite songs, delete songs, retrieve the
    list of artists of the song, songs count and songs length
    """
    @staticmethod
    def get_by_id(id:int)->str:
        
        try:
            data = Song.objects.get(id=id)
        except:
            raise ObjectDoesNotExist(f"No songs with id {id}")

        return data
    
    @staticmethod
    def get_by_name(name:str)->str:

        try:
            data = Song.objects.get(name=name)
        except:
            raise ObjectDoesNotExist(f"No songs with name {name}")

        return data
    
    @staticmethod
    def get_by_match_string(match_string:str)->list:

        # Retrieves the list of songs based on the case insensitive match string
        data = Song.objects.filter(name__icontains=match_string).values_list('name', flat=True)
        
        if not data:
            raise ObjectDoesNotExist(f"No songs with match_string {match_string}")
        
        return list(data)
    
    @staticmethod
    def get_all()->list:

        data = Song.objects.all().values_list('name', flat=True)
        
        if not data:
            raise ObjectDoesNotExist("No songs found")

        return list(data)
    
    @staticmethod
    def get_songs_count()->int:

        try:
            count = Song.objects.count()
        except:
            raise ObjectDoesNotExist("No songs found")
        
        return count
    
    @staticmethod
    def get_songs_length()->float:

        try:
            songs_length = Song.objects.aggregate(Sum('length'))
        except:
            raise ObjectDoesNotExist("No songs found")
        else:
            if songs_length.get('length__sum'):
                songs_length_in_mins = songs_length.get('length__sum')/60.0
            else:
                songs_length_in_mins = 0

        return songs_length_in_mins
    
    @staticmethod
    def get_artists_by_name(song_name:str)->list:

        # Retrieves the list of artists based on case insensitive song name
        data = Song.objects.filter(name__iexact=song_name).values_list('artist', flat=True)

        if not data:
            raise ObjectDoesNotExist(f"No song found with name {song_name}")
        
        return list(data)
    
    @staticmethod
    def get_artists_by_id(id:str)->list:

        data = Song.objects.filter(id=id).values_list('artist', flat=True)

        if not data:
            raise ObjectDoesNotExist(f"No song found with id {id}")
        
        return list(data)

    @staticmethod
    def create(name:str, artists:str, album:str, length:int)->bool:

        try:
            new_song = Song.objects.create(
                name=name,
                artist=artists,
                album=album,
                length=length
            )
        except ValueError:
            raise DataError("Song hasn't been saved")
        else:
            new_song.save()
            return True
        
        return False

    @staticmethod
    def delete(id:int)->bool:

        try:
            song_deleted = Song.objects.get(id=id)
        except:
            raise ObjectDoesNotExist(f"Song with id {id} not found")
        else:
            song_deleted.delete()
            return True
        
        return False
