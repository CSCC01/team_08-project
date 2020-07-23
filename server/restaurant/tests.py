from django.test import TestCase, RequestFactory
from restaurant.models import Food, ManualTag
from django.forms.models import model_to_dict
from django.test import Client
from restaurant.models import Restaurant
import restaurant.views as view_response
import json


class TagClearCases(TestCase):

    def setUp(self):
        """
        Create restaurant food, tag and food object for testing
        """
        self.restaurant = Restaurant.objects.create(name="RestA", address="123 Road", phone=None, email="RA@mail.com",
                                                    city="Toronto",
                                                    cuisine="Chinese", pricepoint="High", twitter="?", instagram="?",
                                                    bio=None,
                                                    GEO_location="?", external_delivery_link="?",
                                                    cover_photo_url="picA",
                                                    logo_url="urlA", rating="4.5")

        self.food = Food.objects.create(name="foodA", restaurant_id=str(self.restaurant._id), description="descripA",
                                        picture="picA",
                                        price=10.99)
        self.tag = ManualTag.objects.create(foods=[self.food._id], category="PR", value="50% off")
        self.food.tags = [self.tag._id]
        self.food.save()
        Food.objects.create(name="foodB", restaurant_id=self.restaurant._id, description="descripB", picture="picB",
                            price=20.99)
        self.factory = RequestFactory()

    def test_clear_tags(self):
        """Test if tag ids are cleared from food document"""
        req = self.factory.post('/api/restaurant/tag/clear/', {'food_name': 'foodA',
                                                               'restaurant_id': str(self.restaurant._id)},
                                content_type='application/json')
        request = self.factory.post('/api/user/role_reassign/', {"user_email": "B@mail.com", "role": "BU"}, content_type='application/json')

        view_response.clear_tags_page(req)
        self.food.refresh_from_db()
        self.assertListEqual(self.food.tags, [])

    def test_clear_foods(self):
        """ Test if food ids are cleared from tag document"""
        req = self.factory.post('/api/restaurant/tag/clear/', {'food_name': 'foodA',
                                                               'restaurant_id': str(self.restaurant._id)},
                                content_type='application/json')
        view_response.clear_tags_page(req)
        self.tag.refresh_from_db()
        self.assertListEqual(self.tag.foods, [])


class AddTagCase(TestCase):
    def setUp(self):
        """Load food, tag documents and json data for food"""
        self.food = Food.objects.create(name="foodA", restaurant_id='mock',
                                        description="descripA", picture="picA",
                                        price=10.99)
        self.tag = ManualTag.objects.create(foods=[], category="PR", value="50% off")
        self.data1 = {
            "food_name": 'foodA',
            'category': 'PR',
            'restaurant_id': 'mock',
            'value': '50% off'
        }
        self.data2 = {
            "food_name": 'foodA',
            'category': 'PR',
            'restaurant_id': 'mock',
            'value': '30% off'
        }

        self.factory = RequestFactory()

    def test_food_ids(self):
        """ Test if a tag's food list has been updated given tag exists"""
        req = self.factory.post('/api/restaurant/tag/insert', self.data1, content_type='application/json')
        view_response.insert_tag_page(req)
        self.tag.refresh_from_db()
        self.assertListEqual([self.food._id], self.tag.foods)

    def test_tag_ids(self):
        """ Test food's tag list has been updated given tag exists"""
        req = self.factory.post('/api/restaurant/tag/insert', self.data1, content_type='application/json')
        view_response.insert_tag_page(req)
        self.food.refresh_from_db()
        self.assertListEqual([self.tag._id], self.food.tags)

    def test_tag_creation(self):
        """ Test if new tag document was created upon tagging"""
        req = self.factory.post('/api/restaurant/tag/insert', self.data2, content_type='application/json')
        view_response.insert_tag_page(req)
        self.tag = ManualTag.objects.get(value='30% off', category='PR')
        self.assertListEqual([self.food._id], self.tag.foods)

    def test_foods_already_tagged(self):
        """ Test tag's foods list if already tagged"""
        # tag food/tags
        self.tag.foods = [self.food._id]
        self.food.tags = [self.tag._id]
        self.food.save()
        self.tag.save()

        req = self.factory.post('/api/restaurant/tag/insert', self.data1, content_type='application/json')
        view_response.insert_tag_page(req)

        # ensure no double tagging
        self.assertListEqual(self.tag.foods, [self.food._id])

    def test_tags_already_tagged(self):
        """Test food's tags if already tagged"""
        # tag food/tags
        self.tag.foods = [self.food._id]
        self.food.tags = [self.tag._id]
        self.food.save()
        self.tag.save()

        req = self.factory.post('/api/restaurant/tag/insert', self.data1, content_type='application/json')
        view_response.insert_tag_page(req)

        # ensure no double tagging
        self.assertListEqual(self.food.tags, [self.tag._id])


class AutoTag(TestCase):
    def setUp(self):
        """Load food document"""
        self.food = Food.objects.create(name="foodA", restaurant_id='mock',
                                        description="chicken", picture="picA",
                                        price='10.99')
        self.factory = RequestFactory()

    def test_auto(self):
        """ Test if food description generates correct tags"""
        request = self.factory.post('/api/restaurant/tag/auto/', {'_id': str(self.food._id)},
                                    content_type="application/json")
        actual = json.loads(view_response.auto_tag_page(request).content)['tags'][0]
        expected = model_to_dict(ManualTag.objects.get(category='DI', value='chicken'))
        expected['_id'] = str(expected['_id'])
        expected['foods'] = [str(food) for food in expected['foods']]
        self.assertDictEqual(expected, actual)


class FoodTestCases(TestCase):

    def setUp(self):
        """ Load food document"""
        self.foodA = Food.objects.create(name="foodA", restaurant_id="restA", description="descripA", picture="picA",
                                         price='10.99')
        self.foodB = Food.objects.create(name="foodB", restaurant_id="restB", description="descripB", picture="picB",
                                         price='20.99')
        self.factory = RequestFactory()

    def test_get_all_foods(self):
        """Test if all foods from db are retrieved"""
        req = self.factory.get('api/restaurant/get_all')
        actual = json.loads(view_response.all_dishes_page(req).content)
        expected = {'Dishes': [model_to_dict(self.foodA), model_to_dict(self.foodB)]}
        expected['Dishes'][0]['_id'] = str(expected['Dishes'][0]['_id'])
        expected['Dishes'][1]['_id'] = str(expected['Dishes'][1]['_id'])
        self.assertDictEqual(expected, actual)

    def test_delete_food(self):
        """Test if the food is deleted"""
        req = self.factory.post('api/restaurant/dish/delete', {'food_name': "foodA","restaurant_id": "restA"},
                                content_type="application/json")
        view_response.delete_dish_page(req)
        actual = Food.objects.filter(name="foodA").first()
        expected = None
        self.assertEqual(expected, actual)

class RestaurantTestCase(TestCase):

    def setUp(self):
        """Load json data for restaurants"""
        self.maxDiff = None
        self.expected = {
            '_id': '111111111111111111111111',
            'name': 'kfc',
            'address': '211 oakland',
            'phone': 6475040680,
            'city': 'markham',
            'email': 'alac@gmail.com',
            'cuisine': 'american',
            'pricepoint': 'High',
            'twitter': 'https://twitter.com/SupremeDreams_1',
            'instagram': 'https://www.instagram.com/rdcworld1/?hl=en',
            'bio': 'Finger licking good chicken',
            'GEO_location': '{\'longitude\': 44.068203, \'latitude\':-114.742043}',
            'external_delivery_link': 'https://docs.djangoproject.com/en/topics/testing/overview/',
            'cover_photo_url': 'link',
            'logo_url': 'link',
            'rating': '3.00'
        }

        self.expected2 = {
            '_id': '000000000000000000000000',
            'name': 'Calvins curry',
            'address': '211 detroit',
            'phone': 6475040680,
            'city': 'markham',
            'email': 'calvin@gmail.com',
            'cuisine': 'african',
            'pricepoint': 'Medium',
            'twitter': 'https://twitter.com/SupremeDreams_1',
            'instagram': 'https://www.instagram.com/rdcworld1/?hl=en',
            'bio': 'Finger licking good chicken',
            'GEO_location': '{\'longitude\': 44.068203, \'latitude\':-114.742043}',
            'external_delivery_link': 'https://docs.djangoproject.com/en/topics/testing/overview/',
            'cover_photo_url': 'link',
            'logo_url': 'link',
            'rating': '3.00'
        }

        self.expected3 = {
            '_id': '222222222222222222222222',
            'name': 'Winnies lambs',
            'address': '211 chicago',
            'phone': 6475040680,
            'city': 'Chicago',
            'email': 'winnie@gmail.com',
            'cuisine': 'asina fusion',
            'pricepoint': 'High',
            'twitter': 'https://twitter.com/SupremeDreams_1',
            'instagram': 'https://www.instagram.com/rdcworld1/?hl=en',
            'bio': 'Finger licking good chicken',
            'GEO_location': '{\'longitude\': 44.068203, \'latitude\':-114.742043}',
            'external_delivery_link': 'https://docs.djangoproject.com/en/topics/testing/overview/',
            'cover_photo_url': 'link',
            'logo_url': 'link',
            'rating': '3.00'
        }

        Restaurant.objects.create(**self.expected)
        Restaurant.objects.create(**self.expected2)
        self.factory = RequestFactory()

    def test_find_restaurant(self):
        """ Test if correct restaurant is retrieved given id"""
        request = self.factory.get('/api/restaurant/get/', {'_id': '111111111111111111111111'},
                                   content_type="application/json")
        self.assertDictEqual(self.expected, json.loads(view_response.get_restaurant_page(request).content))

    def test_find_all_restaurant(self):
        """ Test if all restaurant documents are returned"""
        request = self.factory.get('/api/restaurant/get_all/')
        expected = [self.expected, self.expected2]
        actual = json.loads(view_response.get_all_restaurants_page(request).content)['Restaurants']
        self.assertListEqual(expected, actual)

    def test_insert_restaurant(self):
        """ Test is restaurant is properly inserted into the database"""
        request = self.factory.post('/api/restaurant/insert/', self.expected3, content_type="application/json")
        actual = json.loads(view_response.insert_restaurant_page(request).content)
        self.assertDictEqual(self.expected3, actual)

    def test_edit_restaurant(self):
        """ Test if restaurant document is properly updated"""
        id = Restaurant.objects.get(_id="111111111111111111111111")._id
        request = self.factory.post('/api/restaurant/edit/',
                                    {"restaurant_id": "111111111111111111111111", "name": "kfc2",
                                     "address": "211 Cambodia", "phone": "", "city": "", "email": "", "cuisine": "",
                                     "pricepoint": "", "twitter": "", "instagram": "", "bio": "", "GEO_location": "",
                                     "external_delivery_link": "", "cover_photo_url": "", "logo_url": "",
                                     "rating": "1.00"
                                     }, content_type='application/json')
        view_response.edit_restaurant_page(request)
        actual = Restaurant.objects.get(_id="111111111111111111111111")
        expected = Restaurant(_id=id, name='kfc2',
                              address='211 Cambodia', phone=6475040680, city='markham', email='alac@gmail.com',
                              cuisine='american', pricepoint='High', twitter='https://twitter.com/SupremeDreams_1',
                              instagram='https://www.instagram.com/rdcworld1/?hl=en',
                              bio='Finger licking good chicken',
                              GEO_location='{\'longitude\': 44.068203, \'latitude\':-114.742043}',
                              external_delivery_link='https://docs.djangoproject.com/en/topics/testing/overview/',
                              cover_photo_url='link', logo_url='link', rating='1.00')
        self.assertEqual(actual, expected)
