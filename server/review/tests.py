import json

from bson import ObjectId
from django.forms import model_to_dict
from django.test import TestCase, RequestFactory

from restaurant.models import Restaurant
from review.models import Review
import review.views as view_response

# Create your tests here.

MOCK_VALID_LINK = 'http://link'


class ReviewCases(TestCase):

    def setUp(self):
        """ Create restaurant food, tag and food object for testing """
        self.review = Review.objects.create(restaurant_id="RestA", user_email="test@mail.com", title="title",
                                            content="content", rating=4)
        self.review2 = Review.objects.create(restaurant_id="RestA", user_email="test3@mail.com", title="title3",
                                             content="content3", rating=5)
        self.expected = {"restaurant_id": "111111111111111111111111", "user_email": "new@mail.com",
                         "title": "title2", "content": "content2",
                         "rating": 3}
        self.expected2 = {"restaurant_id": "111111111111111111111111", "user_email": "new@mail.com",
                         "title": "title3", "content": "content3",
                         "rating": 4}
        Restaurant.objects.create(**{
            '_id': '111111111111111111111111', 'name': 'kfc', 'address': '211 oakland', 'phone': 6475040680,
            'city': 'markham', 'email': 'alac@gmail.com', 'cuisine': 'american', 'pricepoint': 'High',
            'twitter': MOCK_VALID_LINK, 'instagram': MOCK_VALID_LINK, 'bio': 'Finger licking good chicken',
            'GEO_location': '{\'longitude\': 44.068203, \'latitude\':-114.742043}',
            'external_delivery_link': MOCK_VALID_LINK,
            'cover_photo_url': MOCK_VALID_LINK, 'logo_url': MOCK_VALID_LINK, 'owner_name': 'Colonel Sanders',
            'owner_story': 'i made chicken', 'owner_picture_url': MOCK_VALID_LINK, 'categories': []})
        self.factory = RequestFactory()

    def test_insert_review(self):
        """ Test if the review document is inserted properly """
        req = self.factory.post('/api/review/insert/', self.expected, content_type='application/json')
        actual = json.loads(view_response.insert_review_page(req).content)
        del actual['Timestamp']
        expected = Review(_id=actual['_id'], restaurant_id="111111111111111111111111", user_email="new@mail.com",
                          title="title2",
                          content="content2", rating=3)
        self.assertDictEqual(model_to_dict(expected), actual)

    def test_get_restaurant_reviews(self):
        """ Test if the correct reviews are returned """
        req = self.factory.get('/api/review/get/', {'restaurant_id': 'RestA'}, content_type='application/json')
        actual = json.loads(view_response.get_restaurant_reviews_page(req).content)
        for dish in actual['Reviews']:
            del dish['Timestamp']
            dish['_id'] = ObjectId(dish['_id'])
        expected = {'Reviews': [model_to_dict(self.review), model_to_dict(self.review2)]}
        self.assertDictEqual(expected, actual)

    def test_insert_review_rating(self):
        """ Test the rating if the restaurant ratings is reflective of average review ratings """
        req = self.factory.post('/api/review/insert/', self.expected, content_type='application/json')
        req2 = self.factory.post('/api/review/insert/', self.expected2, content_type='application/json')
        view_response.insert_review_page(req)
        view_response.insert_review_page(req2)
        actual = Restaurant.objects.get(_id=ObjectId('111111111111111111111111')).rating
        expected = '3.50'
        self.assertEqual(expected, actual)
