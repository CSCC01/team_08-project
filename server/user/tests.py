from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory
from user.views import *
from restaurant.models import Restaurant
from user.models import SDUser
from user.enum import Roles


class SDUserTestCases(TestCase):

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

    # Tests the signup view with valid parameters by calling it then checking the database to see if it exists
    def test_signup(self):
        request = self.factory.post('/api/user/signup/', {"nickname": "TesterA", "name": "Tester", "picture": "picA",
                                                          "updated_at": "2020-06-26T14:07:39.888Z",
                                                          "email": "A@mail.com", "email_verified": True, "role": "BU",
                                                          "restaurant_id": ""}, content_type='application/json')
        actual = signup_page(request).content
        expected = {"nickname": "TesterA", "name": "Tester", "picture": "picA",
                    "last_updated": "2020-06-26T14:07:39.888Z",
                    "email": "A@mail.com", "email_verified": True, "role": "BU",
                    "restaurant_id": None}
        self.assertJSONEqual(actual, expected)

    # Tests the signup view by calling it with invalid role then checking if the proper error is thrown
    def test_signup_invalid_role(self):
        self.assertRaises(ValidationError, SDUser.signup, "TesterF", "Tester", "picF", "2020-06-26T14:07:39.888Z",
                          "F@mail.com", True, "Random", "")

    # Tests the reassign view (Downgrading from RO -> BU) by calling it then checking the database to see if the
    # changes were made
    def test_reassign_RO_to_BU(self):
        request = self.factory.post('/api/user/role_reassign/', {"user_email": "B@mail.com", "role": "BU"},
                                    content_type='application/json')
        reassign_page(request)
        actual = SDUser.objects.get(pk="B@mail.com").role
        expected = "BU"
        self.assertEqual(actual, expected)

    # Tests the reassign view (Upgrading from BU -> RO) by calling it then checking the database to see if the
    # changes were made ABC123
    def test_reassign_BU_to_RO_User(self):
        """
        Tests the reassign view (Upgrading from BU -> RO) by calling it then checking the database
        to see if the changes were made on the SDUser Document
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

        self.assertDictEqual(model_to_dict(actual), model_to_dict(expected))

    def test_reassign_BU_to_RO_Restaurant(self):
        """
        Tests the reassign view (Upgrading from BU -> RO) by calling it then checking the database
        to see if the changes were made on the Restaurant Document
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
        actual = Restaurant.objects.get(email="calvin@gmail.com")
        expected = Restaurant(_id=actual._id, name='Rando Resto',
                              address='211 detroit', phone=6475210680, city='toronto', email='calvin@gmail.com',
                              cuisine='african', pricepoint='Medium', twitter='https://twitter.com/SupremeDreams_s1',
                              instagram='https://www.instagram.com/rdcworld1/2?hl=en',
                              bio='Finger licking good chicken',
                              GEO_location="{\"longitude\": 44.068203, \"latitude\":-114.742043}",
                              external_delivery_link='https://docs.djang22oproject.com/en/topics/testing/overview/',
                              cover_photo_url='link', logo_url='link', rating='3.00')
        self.assertDictEqual(model_to_dict(actual), model_to_dict(expected))

    # Tests the data view by calling it with a valid email and checking if the correct data is returned
    def test_data(self):
        request = self.factory.get('/api/user/data/', {'email': 'E@mail.com'})
        response = data_page(request)
        expected = {"nickname": "TesterE", "name": "Tester", "picture": "picE",
                    "updated_at": "2020-06-26T14:07:39.888Z", "email": "E@mail.com", "email_verified": True,
                    "role": "BU"}
        actual = response.content
        self.assertJSONEqual(actual, expected)

    # Tests the exists view by calling it with an email that exists and checking if True is returned
    def test_exists_true(self):
        request = self.factory.get('/api/user/exists/', {'email': 'B@mail.com'})
        response = exists_page(request)
        expected = {"exists": True}
        actual = response.content
        self.assertJSONEqual(actual, expected)

    # Tests the exists view by calling it with an email that does not exist and checking if False is returned
    def test_exists_false(self):
        request = self.factory.get('/api/user/exists/', {'email': '123B@mail.com'})
        response = exists_page(request)
        expected = {"exists": False}
        actual = response.content
        self.assertJSONEqual(actual, expected)
