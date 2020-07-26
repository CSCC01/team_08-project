from django.test import TestCase
from cloud_storage import cloud_controller
from google.cloud import storage
from PIL import ImageChops
from PIL import Image
from io import BytesIO
import requests


class Upload(TestCase):

    def setUp(self):
        """setup image path, bucket client and delete function"""
        self.path = 'cloud_storage/test_images/image.jpg'
        self.client = storage.Client.from_service_account_json('scdining.json')
        self.delete = lambda path, client: client.bucket('test-storage-nog'). \
            delete_blob(path.replace('https://storage.googleapis.com/test-storage-nog/', ''))

    def test_upload(self):
        """Test is file has been uploaded to the bucket"""
        with open(self.path, "rb") as file:
            path = cloud_controller.upload(file, cloud_controller.TEST_BUCKET)
        response = requests.get(path)  # download image content
        self.delete(path, self.client)
        self.assertTrue(ImageChops.difference(Image.open(self.path),
                                              Image.open(BytesIO(response.content))))


class Delete(TestCase):

    def setUp(self):
        """Upload image to bucket"""
        self.name = 'test'
        blob = storage.Client.from_service_account_json('scdining.json').bucket('test-storage-nog').blob(self.name)
        blob.upload_from_filename('cloud_storage/test_images/image.jpg')
        self.path = 'https://storage.googleapis.com/test-storage-nog/test'

    def test_delete(self):
        """Test if file has been erased from bucket"""
        cloud_controller.delete('https://storage.googleapis.com/test-storage-nog/test')
        expected = 404
        actual = requests.get('https://storage.googleapis.com/test-storage-nog/test').status_code
        self.assertEqual(expected, actual)


class DeleteDefault(TestCase):

    def setUp(self):
        """upload image to asset"""
        client = storage.Client.from_service_account_json('scdining.json')
        blob = client.bucket('default-assets').blob('test')
        blob.upload_from_filename('cloud_storage/test_images/image.jpg')
        self.path = 'https://storage.googleapis.com/default-assets/test'
        self.bucket = client.bucket('default-assets')

    def test_delete_default(self):
        """Test if file has not been erased from bucket"""
        cloud_controller.delete(self.path)
        response = requests.get(self.path)  # download image content
        self.bucket.delete_blob('test')
        self.assertEqual(response.status_code, 200)