from django.test import TestCase, RequestFactory
from timeline.models import TimelinePost, TimelineComment
from timeline import views as server
import datetime
import json
from bson import ObjectId


class PostSuite(TestCase):

    def setUp(self):
        self.data = {
            '_id': '222222222222222222222222',
            'restaurant_id': '000000000000000000000000',
            'user_id': '111111111111111111111111',
            'content': 'Post',
        }
        self.data2 = {
            '_id': '333333333333333333333333',
            'restaurant_id': '000000000000000000000000',
            'user_id': '111111111111111111111111',
            'content': 'Post',
            'comments': [],
            'likes': [],
        }
        self.data3 = {
            '_id': '444444444444444444444444',
            'restaurant_id': '111111111111111111111111',
            'user_id': '111111111111111111111111',
            'content': 'Post3',
            'comments': [],
            'likes': [],
        }
        TimelinePost.objects.create(**self.data2)
        TimelinePost.objects.create(**self.data3)

    def testUpload(self):
        """Test post data is added to the database"""
        request = RequestFactory().post('api/timeline/post/upload/', self.data, content_type='application/json')
        response = server.upload_post_page(request)
        actual = json.loads(response.content)
        expected = {
            '_id': '222222222222222222222222',
            'restaurant_id': '000000000000000000000000',
            'user_id': '111111111111111111111111',
            'content': 'Post',
            'likes': [],
            'comments': []
        }
        self.assertDictEqual(actual, expected)

    def test_get_post_by_restaurant(self):
        """ Test if all post documents for a restaurant are returned """
        request = RequestFactory().get('/api/timeline/post/get_by_restaurant/',
                                       {'restaurant_id': '000000000000000000000000'}, content_type='application/json')
        actual = json.loads(server.get_post_by_restaurant_page(request).content)['Posts']
        for post in actual:
            del post['Timestamp']
        expected = [self.data2]
        self.assertListEqual(expected, actual)

class CommentSuite(TestCase):

    def setUp(self):
        self.post = TimelinePost.objects.create(**{
            'restaurant_id': '000000000000000000000000',
            'user_id': '111111111111111111111111',
            'content': 'Post',
        })

    def testUploadComment(self):
        """Test comment data is added to the database"""
        request = RequestFactory().post('api/timeline/timeline/comment/upload/', {
            '_id': '000000000000000000000000',
            'post_id' : str(self.post._id),
            'user_id': '111111111111111111111111',
            'content': 'testing'
        }, content_type='application/json')
        response = server.upload_comment_page(request)
        actual = json.loads(response.content)
        expected = {
            '_id': '000000000000000000000000',
            'post_id': str(self.post._id),
            'user_id': '111111111111111111111111',
            'content': 'testing',
            'likes':[]
        }
        self.assertDictEqual(actual, expected)

    def testUploadPost(self):
        """Test comment id is added to post array"""
        request = RequestFactory().post('api/timeline/timeline/comment/upload/', {
            '_id': '000000000000000000000000',
            'post_id' : str(self.post._id),
            'user_id': '111111111111111111111111',
            'content': 'testing'
        }, content_type='application/json')
        server.upload_comment_page(request)
        self.post.refresh_from_db()
        expected = [ObjectId('000000000000000000000000')]
        actual = self.post.comments
        self.assertListEqual(expected, actual)
