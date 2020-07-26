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

        ## test values for deletion testing
        self.deletepost = {
            '_id': '121212121212121212121212',
            'restaurant_id': '0000000000000000000000',
            'user_id': '111111111111111111111111',
            'content': 'deletethispost'
        }
        self.unrelatedpost = {
            '_id': '333333333333333333333333',
            'restaurant_id': '0000000000000000000000',
            'user_id': '111111111111111111111111',
            'content': 'deletethispost'
        }
        self.relatedcomment = {
            '_id': '111111111111111111111222',
            'post_id': '121212121212121212121212',
            'user_id': '111111111111111111114444',
            'content': 'this post needs to be deleted'
        }
        self.unrelatedcomment = {
            '_id': '111111111111111111111333',
            'post_id': '333333333333333333333333',
            'user_id': '111111111111111111115555',
            'content': 'this post needs to remain'
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
            'comments': []
        }
        self.assertDictEqual(actual, expected)
    

    def testDelete(self):
        """
        Test post with given id is deleted and its related comments, but not unrelated posts or comments
        PREREQUISITES: api/timeline/comment/upload test must pass since deletions require upload setup
        """

        expected_deleted_comment_list = [self.relatedcomment]
        expected_deleted_post = self.deletepost

        #setup post for deletion and dummy post for testing side effects named unrelated, both with comments
        request_delete_post = RequestFactory().post('api/timeline/post/upload', self.deletepost)
        upload_response = server.upload_post_page(request_delete_post)
        
        request_unrelated_post = RequestFactory().post('api/timeline/post/upload', self.unrelatedpost)
        unrelated_upload_response = server.upload_post_page(request_unrelated_post)
        
        request_related_comment = RequestFactory().post('api/timeline/comment/upload', self.relatedcomment)
        related_comment_upload = server.upload_comment_page(request_related_comment)
        
        request_unrelated_comment = RequestFactory().post('api/timeline/comment/upload', self.unrelatedcomment)
        unrelated_comment_upload = server.upload_comment_page(request_unrelated_comment)

        
        
        request_deletion = RequestFactory().post('api/timeline/post/delete', {'post_id': self.deletepost['_id']})
        deletion_response = server.delete_post_page(request_deletion)



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
        response = server.upload_comment(request)
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
        server.upload_comment(request)
        self.post.refresh_from_db()
        expected = [ObjectId('000000000000000000000000')]
        actual = self.post.comments
        self.assertListEqual(expected, actual)