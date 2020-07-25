from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory
from user.views import *
from restaurant.models import Restaurant
from user.models import SDUser
from user.enum import Roles


class SDUserTestCases(TestCase):
    """ Load User Documents """

    def setUp(self):
        SDUser.objects.create(nickname="TesterB", name="Tester", picture="picB",
                              last_updated="2020-06-26T14:07:39.888Z", email="B@mail.com", email_verified=True,
                              role=Roles.RO.name, restaurant_id="22222222222222")
        SDUser.objects.create(nickname="TesterC", name="Tester", picture="picC",
                              last_updated="2020-06-26T14:07:39.888Z", email="C@mail.com", email_verified=True,
                              role=Roles.BU.name)
        SDUser.objects.create(nickname="TesterD", name="Tester", picture="picD",
                              last_updated="2020-06-26T14:07:39.888Z", email="D@mail.com", email_verified=True,
                              role=Roles.BU.name)
        SDUser.objects.create(nickname="TesterE", name="Tester", picture="picE",
                              last_updated="2020-06-26T14:07:39.888Z", email="E@mail.com", email_verified=True,
                              role=Roles.BU.name)
        self.factory = RequestFactory()

    def test_signup(self):
        """ Tests the signup view with valid parameters by calling it then checking the database to see if it exists """
        request = self.factory.post('/api/user/signup/', {"nickname": "TesterA", "name": "Tester", "picture": "picA",
                                                          "updated_at": "2020-06-26T14:07:39.888Z",
                                                          "email": "A@mail.com", "email_verified": True, "role": "BU",
                                                          "restaurant_id": ""}, content_type='application/json')
        signup_page(request)
        actual = SDUser.objects.get(pk="A@mail.com")
        expected = SDUser(nickname="TesterA", name="Tester", picture="picA", last_updated="2020-06-26T14:07:39.888Z",
                          email="A@mail.com", email_verified=True, role="BU", restaurant_id=None)
        self.assertEqual(actual, expected)

    def test_signup_invalid_role(self):
        """ Tests the signup view by calling it with invalid role then checking if the proper error is thrown"""
        self.assertRaises(ValidationError, SDUser.signup, "TesterF", "Tester", "picF", "2020-06-26T14:07:39.888Z",
                          "F@mail.com", True, "Random", "")

    def test_reassign_RO_to_BU(self):
        """
        Tests the reassign view (Downgrading from RO -> BU) by calling it then checking the
        database to see if the changes were made
        """
        request = self.factory.post('/api/user/role_reassign/', {"user_email": "B@mail.com", "role": "BU"},
                                    content_type='application/json')
        reassign_page(request)
        actual = SDUser.objects.get(pk="B@mail.com")
        expected = SDUser(nickname="TesterB", name="Tester", picture="picB", last_updated="2020-06-26T14:07:39.888Z",
                          email="B@mail.com", email_verified=True, role="BU", restaurant_id="")
        self.assertEqual(actual, expected)

    def test_reassign_BU_to_RO(self):
        """
        Tests the reassign view (Upgrading from BU -> RO) by calling it then checking the database
        to see if the changes were made
        """
        request = self.factory.post('/api/user/role_reassign/',
                                    {"user_email": "C@mail.com", "role": "RO", "name": "Rando Resto",
                                     "address": "211 detroit", "phone": 6475210680,
                                     "city": "toronto", "email": "calvin@gmail.com",
                                     "cuisine": "african", "pricepoint": "Medium",
                                     "twitter": "https://twitter.com/SupremeDreams_s1",
                                     "instagram": "https://www.instagram.com/rdcworld1/2?hl=en",
                                     "bio": "Finger licking good chicken",
                                     "GEO_location": "{\"longitude\": 44.068203, \"latitude\":-114.742043}",
                                     "external_delivery_link": "https://docs.djang22oproject.com/en/topics/testing/overview/",
                                     "cover_photo_url": "link",
                                     "logo_url": "link",
                                     "rating": "3.00"}, content_type='application/json')
        reassign_page(request)
        restaurant = Restaurant.objects.get(email="calvin@gmail.com")
        actual = SDUser.objects.get(pk="C@mail.com")
        expected = SDUser(nickname="TesterC", name="Tester", picture="picC", last_updated="2020-06-26T14:07:39.888Z",
                          email="C@mail.com", email_verified=True, role="RO", restaurant_id=str(restaurant._id))
        self.assertEqual(actual, expected)

    def test_data(self):
        """ Tests the data view by calling it with a valid email and checking if the correct data is returned """
        request = self.factory.get('/api/user/data/', {'email': 'E@mail.com'})
        response = data_page(request)
        expected = {"nickname": "TesterE", "name": "Tester", "picture": "picE",
                    "updated_at": "2020-06-26T14:07:39.888Z", "email": "E@mail.com", "email_verified": True,
                    "role": "BU"}
        actual = response.content
        self.assertJSONEqual(actual, expected)

    def test_exists_true(self):
        """ Tests the exists view by calling it with an email that exists and checking if True is returned """
        request = self.factory.get('/api/user/exists/', {'email': 'B@mail.com'})
        response = exists_page(request)
        expected = {"exists": True}
        actual = response.content
        self.assertJSONEqual(actual, expected)

    def test_exists_false(self):
        """ Tests the exists view by calling it with an email that does not exist and checking if False is returned """
        request = self.factory.get('/api/user/exists/', {'email': '123B@mail.com'})
        response = exists_page(request)
        expected = {"exists": False}
        actual = response.content
        self.assertJSONEqual(actual, expected)
