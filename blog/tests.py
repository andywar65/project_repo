from datetime import datetime
from django.test import TestCase
from .models import (Location, )

class LocationTestCase(TestCase):
    #@classmethod
    #def setUpTestData(cls):
    def setUp(self):
        Location.objects.create(title="Marco",
            #image = cls.img,
            address="Via Agnelli",
            gmap_link = 'https://goo.gl/maps/jLKe3iur2EtL8zuB7',
            gmap_embed = '<scrap>https://goo.gl/maps/jLKe3iur2EtL8zuB7</scrap>',
            body = 'Body')

    def test_name(self):
        """Name is correctly identified"""
        luogo = Location.objects.get(title="Marco")
        self.assertEqual(luogo.__str__(), 'Marco')

    def test_link(self):
        """Link is correctly identified"""
        luogo = Location.objects.get(title="Marco")
        self.assertEqual(luogo.get_gmap_link(),
            '<a href="https://goo.gl/maps/jLKe3iur2EtL8zuB7" class="btn" target="_blank">Mappa</a>')

    def test_thumb(self):
        """Thumbnail is correctly identified"""
        luogo = Location.objects.get(title="Marco")
        self.assertEqual(luogo.get_thumb(),
            '')
