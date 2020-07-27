from django.forms import model_to_dict
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
        d2 = TimelinePost.objects.create(**self.data2)

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
            'comments': [],
        }
        self.assertDictEqual(actual, expected)

    def test_get_all_post(self):
        """ Test if all post documents are returned """
        request = RequestFactory().get('/api/timeline/post/get_all/')
        actual = json.loads(server.get_all_posts_page(request).content)['Posts']
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
        self.post2 = TimelinePost.objects.create(**{
            'restaurant_id': '222222222222222222222222',
            'user_id': '111111111111111111111111',
            'content': 'Post',
            'comments': []
        })
        self.comment = TimelineComment.objects.create(**{
            '_id': '333333333333333333333333',
            'post_id': self.post2._id,
            'user_id': '111111111111111111111111',
            'likes': [],
            'content': "To be deleted"
        })
        self.post2.comments = [self.comment._id]
        self.post2.save()



    def testUploadComment(self):
        """Test comment data is added to the database"""
        request = RequestFactory().post('api/timeline/comment/upload/', {
            '_id': '000000000000000000000000',
            'post_id': str(self.post._id),
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
            'likes': []
        }
        self.assertDictEqual(actual, expected)

    def test_comment_delete_comment(self):
        """ Test comment is deleted from comment side """
        request = RequestFactory().post('api/timeline/comment/delete/', {
            '_id': '333333333333333333333333',
        }, content_type='application/json')
        server.delete_comment_page(request)
        expected = None
        actual = TimelineComment.objects.filter(_id="333333333333333333333333").first()
        self.assertEquals(expected, actual)

    def test_comment_delete_post(self):
        """ Test comment is deleted from post side """
        request = RequestFactory().post('api/timeline/comment/delete/', {
            '_id': '333333333333333333333333',
        }, content_type='application/json')
        server.delete_comment_page(request)
        expected = []
        actual = TimelinePost.objects.get(_id=ObjectId(str(self.post2._id))).comments
        self.assertListEqual(expected, actual)
        
    def testUploadPost(self):
        """Test comment id is added to post array"""
        request = RequestFactory().post('api/timeline/comment/upload/', {
            '_id': '000000000000000000000000',
            'post_id': str(self.post._id),
            'user_id': '111111111111111111111111',
            'content': 'testing'
        }, content_type='application/json')
        server.upload_comment_page(request)
        self.post.refresh_from_db()
        expected = [ObjectId('000000000000000000000000')]
        actual = self.post.comments
        self.assertListEqual(expected, actual)

    def test_get_comment(self):
        """ Test if correct comment is retrieved given id """
        request = RequestFactory().get('/api/timeline/comment/get/', {'_id': "333333333333333333333333"},
                                       content_type="application/json")
        actual = json.loads(server.get_comment_data_page(request).content)
        del actual['Timestamp']
        expected = {'_id': '333333333333333333333333', 'post_id': str(self.post2._id),
                    'user_id': '111111111111111111111111', 'likes': [], 'content': 'To be deleted'}
        self.assertDictEqual(expected, actual)
