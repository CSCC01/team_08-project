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

        ## test values for deletion testing
        self.deletepost = {
            '_id': '121212121212121212121212',
            'restaurant_id': '0000000000000000000000',
            'user_id': '111111111111111111111111',
            'content': 'deletethispost',
            'comments': [],
            'likes': []
        }
        self.unrelatedpost = {
            '_id': '333333333333333333333334',
            'restaurant_id': '0000000000000000000000',
            'user_id': '111111111111111111111111',
            'content': 'deletethispost',
            'likes': [],
            'comments': []
        }
        self.relatedcomment = {
            '_id': '111111111111111111111222',
            'post_id': '121212121212121212121212',
            'user_id': '111111111111111111114444',
            'content': 'this post needs to be deleted',
            'likes': []
        }
        self.unrelatedcomment = {
            '_id': '111111111111111111111333',
            'post_id': '333333333333333333333333',
            'user_id': '111111111111111111115555',
            'content': 'this post needs to remain',
            'likes': []
        }
        ## test values for deletion testing

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

    def testDelete(self):
        """
        Test post with given id is deleted and its related comments, but not unrelated posts or comments
        PREREQUISITES: api/timeline/comment/upload test must pass since deletions require upload setup
        """

        expected_deleted_comment_list = [self.relatedcomment]
        expected_deleted_post = self.deletepost.copy()
        expected_deleted_post['comments'] = [self.relatedcomment['_id']]

        # setup post for deletion and dummy post for testing side effects named unrelated, both with comments
        request_delete_post = RequestFactory().post('api/timeline/post/upload', self.deletepost,
                                                    content_type='application/json')
        upload_response = server.upload_post_page(request_delete_post)

        request_unrelated_post = RequestFactory().post('api/timeline/post/upload', self.unrelatedpost,
                                                       content_type='application/json')
        unrelated_upload_response = server.upload_post_page(request_unrelated_post)

        request_related_comment = RequestFactory().post('api/timeline/comment/upload', self.relatedcomment,
                                                        content_type='application/json')
        related_comment_upload = server.upload_comment_page(request_related_comment)

        request_unrelated_comment = RequestFactory().post('api/timeline/comment/upload', self.unrelatedcomment,
                                                          content_type='application/json')
        unrelated_comment_upload = server.upload_comment_page(request_unrelated_comment)

        request_deletion = RequestFactory().post('api/timeline/post/delete', {'post_id': self.deletepost['_id']},
                                                 content_type='application/json')
        deletion_response = server.delete_post_page(request_deletion)
        response_dict = json.loads(deletion_response.content)
        actual_deleted_comment_list = response_dict['comments']
        actual_deleted_post = response_dict['post']

        self.assertListEqual(actual_deleted_comment_list, expected_deleted_comment_list)
        self.assertDictEqual(actual_deleted_post, expected_deleted_post)

    def test_get_all_post(self):
        """ Test if all post documents are returned """
        request = RequestFactory().get('/api/timeline/post/get_all/')
        actual = json.loads(server.get_all_posts_page(request).content)['Posts']
        for post in actual:
            del post['Timestamp']
        expected = [self.data2, self.data3]
        self.assertListEqual(expected, actual)

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
