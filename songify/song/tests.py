from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from .models import Song
from .database import DatabaseFunctions

class SongViewTests(TestCase):
    """
    Tests to check various operations performed to favorite list
    """
    def setUp(self):
        """
        Test Data
        """
        self.data1 = dict(
            name="No guidance",
            artist="{Drake, Chris Brown}",
            album="Guide",
            length=300
        )

        self.data2 = dict(
            name="Going Bad",
            artist="{Drake}",
            album="Guidance",
            length=300
        )

        self.songs_url = reverse('songify:songs-name')

        self.client.post(self.songs_url, self.data1)
        self.client.post(self.songs_url, self.data2)
    
    def test_song_count(self):
        """
        Test to check the songs count
        """
        count = DatabaseFunctions.get_songs_count()
        self.assertEqual(count, 2)
    
    def test_song_length(self):
        """
        Test to check the songs length
        """
        total_length = DatabaseFunctions.get_songs_length()
        self.assertEqual(total_length, 10.0)
    
    def test_get_all_songs(self):
        """
        Test to verify all the songs
        """
        all_songs = DatabaseFunctions.get_all()
        self.assertEqual(all_songs, ["No guidance", "Going Bad"])
    
    def test_get_by_name(self):
        """
        Test to get the songs when name is passed as query param
        """
        query_params = urlencode({
            'name': 'No guidance'
        })
        self.url = reverse('songify:songs-name')
        response = self.client.get(f"{self.url}?{query_params}")
        self.assertEqual(response.content.decode('ascii'), "No guidance")
    
    def test_get_by_match_string(self):
        # TODO
        pass

    def test_get_artits(self):
        # TODO
        pass

    def test_delete_song(self):
        # TODO
        pass

    def test_create_song(self):
        # TODO
        pass

class ArtistViewTests(TestCase):
    """
    Tests to verify various artists of the songs
    """
    def test_get_artists_name(self):
        # TODO
        pass
