import json

from bson import ObjectId
from django.forms import model_to_dict
from django.test import TestCase, RequestFactory
from review.models import Review
import review.views as view_response


# Create your tests here.


class ReviewCases(TestCase):

    def setUp(self):
        """ Create restaurant food, tag and food object for testing """
        self.review = Review.objects.create(restaurant_id="RestA", user_email="test@mail.com", title="title",
                                            content="content", rating=4)
        self.review2 = Review.objects.create(restaurant_id="RestA", user_email="test3@mail.com", title="title3",
                                             content="content3", rating=5)
        self.expected = {"restaurant_id": "RestB", "user_email": "new@mail.com",
                         "title": "title2", "content": "content2",
                         "rating": 3}
        self.factory = RequestFactory()

    def test_insert_review(self):
        """ Test if the review document is inserted properly """
        req = self.factory.post('/api/review/insert/', self.expected, content_type='application/json')
        actual = json.loads(view_response.insert_review_page(req).content)
        del actual['Timestamp']
        expected = Review(_id=actual['_id'], restaurant_id="RestB", user_email="new@mail.com", title="title2",
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
