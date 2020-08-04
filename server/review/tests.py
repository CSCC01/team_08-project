import json

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

    def test_get_reviews(self):
        """ Test if the correct review is returned """
        req = self.factory.get('/api/review/get/', {'_id': str(self.review._id)}, content_type='application/json')
        actual = json.loads(view_response.get_review_page(req).content)
        del actual['Timestamp']
        self.review._id = str(self.review._id)
        self.assertDictEqual(model_to_dict(self.review), actual)
