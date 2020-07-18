from django.test import TestCase, RequestFactory
from restaurant.models import Food, ManualTag
from django.forms.models import model_to_dict
from django.test import Client
from restaurant.models import Restaurant
import restaurant.views as response
import json


# class TagClearCases(TestCase):
#
#     def setUp(self):
#         """
#         Create restaurant food, tag and food object for testing
#         """
#         self.restaurant = Restaurant.objects.create(**{"name":"RestA", "address":"123 Road", "phone": 6475040680, "email":"RA@mail.com",
#                                                     "city": "Toronto",
#                                                     "cuisine" : "Chinese", "pricepoint" : "?", "twitter" : "?", "instagram" :"?",
#                                                     "bio" : "bio",
#                                                     "GEO_location" : "?", "external_delivery_link" : "?",
#                                                     "cover_photo_url" :"picA",
#                                                     "logo_url" : "urlA", "rating" :"4.5"})
#
#         self.food = Food.objects.create(name="foodA", restaurant_id=str(self.restaurant._id), description="descripA",
#                                         picture="picA",
#                                         price=10.99)
#         self.tag = ManualTag.objects.create(foods=[self.food._id], category="promo", value="50% off")
#         self.food.tags = [self.tag._id]
#         self.food.save()
#         Food.objects.create(name="foodB", restaurant_id=self.restaurant._id, description="descripB", picture="picB",
#                             price=20.99)
#
#     def test_clear_tags(self):
#         """Test if tag ids are cleared from food object"""
#         restaurant = Restaurant.objects.get(name="RestA")
#         ManualTag.clear_food_tags(food_name="foodA", restaurant=restaurant._id)
#         self.food.refresh_from_db()
#
#         self.assertListEqual(self.food.tags, [])
#
#     def test_clear_foods(self):
#         """ Test if food ids are cleared from tag object"""
#         restaurant = Restaurant.objects.get(name="RestA")
#         ManualTag.clear_food_tags(food_name="foodA", restaurant=restaurant._id)
#         self.tag.refresh_from_db()
#
#         self.assertListEqual(self.tag.foods, [])
#
#
# class AddTagCase(TestCase):
#     def setUp(self):
#         self.food = Food.objects.create(name="foodA", restaurant_id='mock',
#                                         description="descripA", picture="picA",
#                                         price=10.99)
#         self.tag = ManualTag.objects.create(foods=[], category="promo", value="50% off")
#
#     def test_foods_list(self):
#         """ Test if a tags food list has been updated given tag exists"""
#         ManualTag.add_tag(food_name='foodA', category='promo', restaurant='mock', value='50% off')
#         self.tag.refresh_from_db()
#         self.assertListEqual([self.food._id], self.tag.foods)
#
#     def test_tags_list(self):
#         """ Test food's tag list has been updated given"""
#         ManualTag.add_tag(food_name='foodA', category='promo', restaurant='mock', value='50% off')
#         self.food.refresh_from_db()
#         self.assertListEqual([self.tag._id], self.food.tags)
#
#     def test_tag_creation(self):
#         """ Test if tag object was created"""
#         ManualTag.add_tag(food_name='foodA', category='promo', restaurant='mock', value='30% off')
#         self.tag = ManualTag.objects.get(value='30% off', category='promo')
#         self.assertListEqual([self.food._id], self.tag.foods)
#
#     def test_foods_already_tagged(self):
#         """ Test foods list on already tagged tag"""
#         self.tag.foods = [self.food._id]
#         self.food.tags = [self.tag._id]
#         self.food.save()
#         self.tag.save()
#         ManualTag.add_tag(food_name='foodA', category='promo', restaurant='mock', value='50% off')
#         self.assertListEqual(self.tag.foods, [self.food._id])
#
#     def test_tags_already_tagged(self):
#         """ Test tags list on already tagged food"""
#         self.tag.foods = [self.food._id]
#         self.food.tags = [self.tag._id]
#         self.food.save()
#         self.tag.save()
#         ManualTag.add_tag(food_name='foodA', category='promo', restaurant='mock', value='50% off')
#         self.assertListEqual(self.food.tags, [self.tag._id])


class AutoTag(TestCase):
    def setUp(self):
        self.food = Food.objects.create(name="foodA", restaurant_id='mock',
                                        description="chicken", picture="picA",
                                        price='10.99')
        self.factory = RequestFactory()

    def test_auto(self):
        """ Test if food description generates correct tags"""
        request = self.factory.post('/api/restaurant/tag/auto/', {'_id': str(self.food._id)})
        print(request.body)
        response.auto_tag_page(request)
        expected = model_to_dict(ManualTag.objects.get(category='dish', value='chicken'))
        expected['_id'] = str(expected['_id'])
        expected['foods'] = [str(food) for food in expected['foods']]
        self.assertDictEqual(expected, actual)


# class FoodTestCases(TestCase):
#
#     def setUp(self):
#         self.foodA = Food.objects.create(name="foodA", restaurant_id="restA", description="descripA", picture="picA",
#                                          price='10.99')
#         self.foodB = Food.objects.create(name="foodB", restaurant_id="restB", description="descripB", picture="picB",
#                                          price='20.99')
#         self.factory = RequestFactory()
#
#     def test_get_all_foods(self):
#         """Test if all foods from db are retrieved"""
#         req = self.factory.get('api/restaurant/get_all')
#         actual = json.loads(response.all_dishes_page(req).content)
#         expected = {'Dishes': [model_to_dict(self.foodA), model_to_dict(self.foodB)]}
#         expected['Dishes'][0]['_id'] = str(expected['Dishes'][0]['_id'])
#         expected['Dishes'][1]['_id'] = str(expected['Dishes'][1]['_id'])
#         self.assertDictEqual(expected, actual)


# class RestaurantTestCase(TestCase):
#
#     def setUp(self):
#         self.maxDiff = None
#         self.expected = {
#             '_id': '111111111111111111111111',
#             'name': 'kfc',
#             'address': '211 oakland',
#             'phone': 6475040680,
#             'city': 'markham',
#             'email': 'alac@gmail.com',
#             'cuisine': 'american',
#             'pricepoint': 'high',
#             'twitter': 'https://twitter.com/SupremeDreams_1',
#             'instagram': 'https://www.instagram.com/rdcworld1/?hl=en',
#             'bio': 'Finger licking good chicken',
#             'GEO_location': '{\'longitude\': 44.068203, \'latitude\':-114.742043}',
#             'external_delivery_link': 'https://docs.djangoproject.com/en/topics/testing/overview/',
#             'cover_photo_url': 'link',
#             'logo_url': 'link',
#             'rating': '3.00'
#         }
#
#         self.expected2 = {
#             '_id': '000000000000000000000000',
#             'name': 'Calvins curry',
#             'address': '211 detroit',
#             'phone': 6475040680,
#             'city': 'markham',
#             'email': 'calvin@gmail.com',
#             'cuisine': 'african',
#             'pricepoint': 'medium',
#             'twitter': 'https://twitter.com/SupremeDreams_1',
#             'instagram': 'https://www.instagram.com/rdcworld1/?hl=en',
#             'bio': 'Finger licking good chicken',
#             'GEO_location': '{\'longitude\': 44.068203, \'latitude\':-114.742043}',
#             'external_delivery_link': 'https://docs.djangoproject.com/en/topics/testing/overview/',
#             'cover_photo_url': 'link',
#             'logo_url': 'link',
#             'rating': '3.00'
#         }
#
#         self.expected3 = {
#             '_id': '222222222222222222222222',
#             'name': 'Winnies lambs',
#             'address': '211 chicago',
#             'phone': 6475040680,
#             'city': 'Chicago',
#             'email': 'winnie@gmail.com',
#             'cuisine': 'asina fusion',
#             'pricepoint': 'high',
#             'twitter': 'https://twitter.com/SupremeDreams_1',
#             'instagram': 'https://www.instagram.com/rdcworld1/?hl=en',
#             'bio': 'Finger licking good chicken',
#             'GEO_location': '{\'longitude\': 44.068203, \'latitude\':-114.742043}',
#             'external_delivery_link': 'https://docs.djangoproject.com/en/topics/testing/overview/',
#             'cover_photo_url': 'link',
#             'logo_url': 'link',
#             'rating': '3.00'
#         }
#
#         Restaurant.objects.create(**self.expected)
#         Restaurant.objects.create(**self.expected2)
#         self.factory = RequestFactory()
#
#     def test_find(self):
#         """ Test if correct restaurant is retrieved given id"""
#         request = self.factory.get('/api/restaurant/get/', {'_id': '111111111111111111111111'},
#                          content_type="application/json")
#         self.assertDictEqual(self.expected, json.loads(response.get_restaurant_page(request).content))
#
#     def test_find_all(self):
#         """ Test if all restuarant objects are returned"""
#         request = self.factory.get('/api/restaurant/get_all/')
#         expected = [self.expected, self.expected2]
#         actual = json.loads(response.get_all_restaurants_page(request).content)['Restaurants']
#         self.assertListEqual(expected,actual)
#
#     def test_insert(self):
#         """ Test is restaurant is properly inserted into the database"""
#         request = self.factory.post('/api/restaurant/insert/', self.expected3, content_type="application/json")
#         actual = json.loads(response.insert_restaurant_page(request).content)
#         self.assertDictEqual(self.expected3, actual)
#
#     def test_edit(self):
#         """ Check if restaurant document is properly updated"""
#         id = Restaurant.objects.get(_id="111111111111111111111111")._id
#         request = self.factory.post('/api/restaurant/edit/',
#                                     {"restaurant_id": "111111111111111111111111", "name": "kfc2",
#                                      "address": "211 Cambodia", "phone": "", "city": "", "email": "", "cuisine": "",
#                                      "pricepoint": "", "twitter": "", "instagram": "", "bio": "", "GEO_location": "",
#                                      "external_delivery_link": "", "cover_photo_url": "", "logo_url": "",
#                                      "rating": "1.00"
#                                      }, content_type='application/json')
#         response.edit_restaurant_page(request)
#         actual = Restaurant.objects.get(_id="111111111111111111111111")
#         expected = Restaurant(_id=id, name='kfc2',
#                               address='211 Cambodia', phone=6475040680, city='markham', email='alac@gmail.com',
#                               cuisine='american', pricepoint='high', twitter='https://twitter.com/SupremeDreams_1',
#                               instagram='https://www.instagram.com/rdcworld1/?hl=en',
#                               bio='Finger licking good chicken',
#                               GEO_location='{\'longitude\': 44.068203, \'latitude\':-114.742043}',
#                               external_delivery_link='https://docs.djangoproject.com/en/topics/testing/overview/',
#                               cover_photo_url='link', logo_url='link', rating='1.00')
#         self.assertEqual(actual, expected)
