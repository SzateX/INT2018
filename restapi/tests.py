from django.test import TestCase
from django.urls import reverse
import json
from rest_framework import status
from INT.models import Place, Picture
from restapi.serializers import PlaceSerializer, PictureSerializer


class GetAllPlacesTest(TestCase):
    def setUp(self):
        Place.objects.create(building_name='PRZ A', room_name='A61')
        Place.objects.create(building_name='PRZ V', room_name='V17')

    def test_get_all_places(self):
        response = self.client.get('/restapi/place/')
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSinglePlaceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Place.objects.create(building_name='PRZ A', room_name='A61')
        Place.objects.create(building_name='PRZ V', room_name='V17')

    def test_get_valid_single_place(self):
        response = self.client.get('/restapi/place/'
                                   + str(Place.objects.get(building_name='PRZ A').pk)
                                   + '/')
        place = Place.objects.get(building_name='PRZ A')
        serializer = PlaceSerializer(place)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_place(self):
        response = self.client.get('/restapi/place/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
