from django.test import TestCase
from django.test import Client
from RO.models import Restaurant
import json


# Create your tests here.


class RestaurantTestCase(TestCase):
    rdc = None

    def setUp(self):
        self.expected = {
            '_id': '111111111111111111111111',
            'name': 'kfc',
            'address': '211 oakland',
            'phone': 6475040680,
            'city': 'markham',
            'email': 'alac@gmail.com',
            'cuisine': 'american',
            'pricepoint': 'high',
            'twitter': 'https://twitter.com/SupremeDreams_1',
            'instagram': 'https://www.instagram.com/rdcworld1/?hl=en',
            'bio': 'Finger licking good chicken',
            'GEO_location': '{\'longitude\': 44.068203, \'latitude\':-114.742043}',
            'external_delivery_link': 'https://docs.djangoproject.com/en/topics/testing/overview/',
            'cover_photo_url' : 'link',
            'logo_url' : 'link',
            'rating' : '3.00'
        }

        self.expected2 = {
            '_id': '000000000000000000000000',
            'name': 'Calvins curry',
            'address': '211 detroit',
            'phone': 6475040680,
            'city': 'markham',
            'email': 'calvin@gmail.com',
            'cuisine': 'african',
            'pricepoint': 'medium',
            'twitter': 'https://twitter.com/SupremeDreams_1',
            'instagram': 'https://www.instagram.com/rdcworld1/?hl=en',
            'bio': 'Finger licking good chicken',
            'GEO_location': '{\'longitude\': 44.068203, \'latitude\':-114.742043}',
            'external_delivery_link': 'https://docs.djangoproject.com/en/topics/testing/overview/',
            'cover_photo_url' : 'link',
            'logo_url' : 'link',
            'rating' : '3.00'
        }

        self.expected3 = {
            '_id': '222222222222222222222222',
            'name': 'Winnies lambs',
            'address': '211 chicago',
            'phone': 6475040680,
            'city': 'Chicago',
            'email': 'winnie@gmail.com',
            'cuisine': 'asina fusion',
            'pricepoint': 'high',
            'twitter': 'https://twitter.com/SupremeDreams_1',
            'instagram': 'https://www.instagram.com/rdcworld1/?hl=en',
            'bio': 'Finger licking good chicken',
            'GEO_location': '{\'longitude\': 44.068203, \'latitude\':-114.742043}',
            'external_delivery_link': 'https://docs.djangoproject.com/en/topics/testing/overview/',
            'cover_photo_url' : 'link',
            'logo_url' : 'link',
            'rating' : '3.00'
        }
        Restaurant.objects.create(**self.expected)
        Restaurant.objects.create(**self.expected2)

    def test_find(self):
        c = Client()
        response = c.get('/api/RO/get/', {'_id': '111111111111111111111111'},
                         content_type="application/json")
        self.assertDictEqual(self.expected, json.loads(response.content))

    def test_find_all(self):
        c = Client()
        response = c.get('/api/RO/getAll/')
        expected = [self.expected, self.expected2]
        self.assertListEqual(expected, json.loads(response.content)['Restaurants'])

    def test_insert(self):
        c = Client()
        response = c.post('/api/RO/insert/', self.expected3, content_type="application/json" )
        self.assertDictEqual(self.expected3, json.loads(response.content))