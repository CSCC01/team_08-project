from django.test import TestCase, Client, RequestFactory
from google.cloud import storage
from PIL import ImageChops
from PIL import Image
from io import BytesIO
import requests
from . import cloud_controller
from .IMediaFactory import factory
from restaurant.models import Restaurant, Food
from user.models import SDUser
from . import views
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from .AppType import AppCollection
from django.forms import model_to_dict
from utils.test_helper import TestHelper
from utils.encoder import BSONEncoder

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


class CloudEndPoints(TestCase):

    def setUp(self):
        """
        Set up mock objects to seperate image upload from saving endpoints
        Setup database objects
        Setup image for testing
        Setup utility function to refactor test case code
        """

        class Mock: # Class for mocking behaviour found in cloud_controller
            TEST_BUCKET = 'test'
            PRODUCTION_BUCKET = 'test'
            IMAGE= 'test'
            def upload(self, file, bucket_path, content_type=None):
                return "test_path"

            def delete(self, file_path):
                return('delete')
        mock = Mock()
        for app in factory: # replace all cloud_controller in imageuploaders with mocks
            factory[app].cloud = mock

        # create objects
        self.restaurant = Restaurant.objects.create(**
            {
                "_id": "5f055ad21f6aa20731363b9d",
                "name": "the dinner cafe",
                "address": "200 chicago st",
                "phone": 6475040680,
                "email": "popeyeschicken@popeyes.ca",
                "city": "chicago",
                "cuisine": "american",
                "pricepoint": "low",
                "twitter": "https://twitter.com/KEEMSTAR",
                "instagram": "https://www.instagram.com/dramaalert/?hl=en",
                "bio": "We server the best chicken in the world! Classic american style",
                "GEO_location": "{\"longitude\": 19.421700, \"latitude\" : 13.216966}",
                "external_delivery_link": "https://play.typeracer.com/",
                "cover_photo_url": "https://www.nautilusplus.com/content/uploads/2016/08/Pexel_junk-food.jpeg",
                "logo_url": "https://storage.googleapis.com/test-storage-nog/FILE-pzummgrsjm-2020-07-28 "
                            "17:44:57.560319.png",
                "rating": "4.00",
                "owner_name": "",
                "owner_story": "",
                "owner_picture_url": ""
            }
        )

        self.Food = Food.objects.create(**
            {
                "_id": "5f08040da28f56c7effc919e",
                "name": "Lamb brisket",
                "description": "nutty brisket",
                "picture": "https://storage.googleapis.com/test-storage-nog/FILE-fkbsvatuph-2020-07-29 "
                           "00:03:15.437858.png",
                "price": "24.99",
                "tags": [
                    "5f13b607d0cafe43f9d4f353",
                    "5f147c5a94c8444e29a53986",
                    "5f1a68df8263153711b745d0"
                ],
                "specials": ""
            }
        )

        self.User = SDUser.objects.create(**
            {
                "nickname": "test",
                "name": "testerB",
                "picture": "https://storage.googleapis.com/test-storage-nog/FILE-stxfoqdpeg-2020-07-29 "
                           "00:05:57.376176.png",
                "last_updated": "2020-06-26T14:07:39.888Z",
                "email": "e@mail.com",
                "email_verified": False,
                "role": "BU",
                "restaurant_id": None
            }
        )

        self.image = SimpleUploadedFile(name='test_image.jpg', content=open('cloud_storage/test_images/image.jpg', 'rb').read()
                                        , content_type='image/jpeg')
        self.helper = TestHelper()

    def test_restaurant_logo(self):
        """Test if database saves image url into restaurant logo url"""
        content_type = "multipart/form-data; boundary=boundary"
        request = RequestFactory().post('/api/cloud_storage/upload/',content_type=content_type)
        # setup multipart request
        self.helper.process_request(request,
            {
            'app': AppCollection.restaurant_RestaurantMedia.name,
            '_id': '5f055ad21f6aa20731363b9d',
            'save_location': 'logo_url'
            },
            {'file': self.image}
        )
        response = views.media_upload_page(request)
        actual = json.loads(response.content)
        expected = json.loads(json.dumps(model_to_dict(self.restaurant), cls=BSONEncoder))
        expected['logo_url'] = 'test_path'
        self.assertDictEqual(actual, expected)

    def test_restaurant_cover_photo(self):
        """Test if database saves image url into restaurant cover photo url"""
        content_type = "multipart/form-data; boundary=boundary"
        request = RequestFactory().post('/api/cloud_storage/upload/',content_type=content_type)
        # setup multipart request
        self.helper.process_request(request,
            {
            'app': AppCollection.restaurant_RestaurantMedia.name,
            '_id': '5f055ad21f6aa20731363b9d',
            'save_location': 'cover_photo_url'
            },
            {'file': self.image}
        )
        response = views.media_upload_page(request)
        actual = json.loads(response.content)
        expected = json.loads(json.dumps(model_to_dict(self.restaurant), cls=BSONEncoder))
        expected['cover_photo_url'] = 'test_path'
        self.assertDictEqual(actual, expected)

    def test_restaurant_owner_photo_url(self):
        """Test if database saves image url into owner picture url"""
        content_type = "multipart/form-data; boundary=boundary"
        request = RequestFactory().post('/api/cloud_storage/upload/',content_type=content_type)
        # setup multipart request
        self.helper.process_request(request,
            {
            'app': AppCollection.restaurant_RestaurantMedia.name,
            '_id': '5f055ad21f6aa20731363b9d',
            'save_location': 'owner_picture_url'
            },
            {'file': self.image}
        )
        response = views.media_upload_page(request)
        actual = json.loads(response.content)
        expected = json.loads(json.dumps(model_to_dict(self.restaurant), cls=BSONEncoder))
        expected['owner_picture_url'] = 'test_path'
        self.assertDictEqual(actual, expected)

    def test_food_picture(self):
        """Test if database saves image url into food picture"""
        content_type = "multipart/form-data; boundary=boundary"
        request = RequestFactory().post('/api/cloud_storage/upload/',content_type=content_type)
        # setup multipart request
        self.helper.process_request(request,
            {
            'app': AppCollection.restaurant_FoodMedia.name,
            '_id': '5f08040da28f56c7effc919e',
            'save_location': 'picture'
            },
            {'file': self.image}
        )
        response = views.media_upload_page(request)
        actual = json.loads(response.content)
        expected = json.loads(json.dumps(model_to_dict(self.Food),  cls=BSONEncoder))
        expected['picture'] = 'test_path'
        self.assertDictEqual(actual, expected)

    def test_owner_picture(self):
        """Test if database saves image url to user picture"""
        content_type = "multipart/form-data; boundary=boundary"
        request = RequestFactory().post('/api/cloud_storage/upload/',content_type=content_type)
        # setup multipart request
        self.helper.process_request(request,
            {
            'app': AppCollection.user_SDUserMedia.name,
            'email': 'e@mail.com',
            'save_location': 'picture'
            },
            {'file': self.image}
        )
        response = views.media_upload_page(request)
        actual = json.loads(response.content)
        expected = json.loads(json.dumps(model_to_dict(self.User), cls=BSONEncoder))
        expected['picture'] = 'test_path'
        self.assertDictEqual(actual, expected)