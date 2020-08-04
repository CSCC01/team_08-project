from django.test import TestCase, RequestFactory
from order.models import Cart, Item
from restaurant.models import Food
import order.views as view_response
import json
from utils.encoder import BSONEncoder
from django.forms import model_to_dict
from order import models
from datetime import datetime
import pytz
from utils.test_helper import MockModule
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


class CartTestCases(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.c1 = Cart.objects.create(restaurant_id='222222222222222222222222', user_email='test2@mail.com', price=0)
        self.f1 = Food.objects.create(name="foodA", restaurant_id='mock',
                                      description="chicken", picture="picA",
                                      price='10.99')
        self.f2 = Food.objects.create(name="foodB", restaurant_id='mock',
                                      description="chicken", picture="picA",
                                      price='10.99')
        self.i = Item.objects.create(cart_id=self.c1._id, food_id=self.f2._id, count=2)

    def test_insert_cart(self):
        """ Test if cart document is inserted into the database """
        req = self.factory.post('/api/order/cart/insert/', {'restaurant_id': '111111111111111111111111',
                                                            'user_email': "tester@mail.com"},
                                content_type='application/json')
        actual = json.loads(view_response.insert_cart_page(req).content)
        expected = {"_id": str(Cart.objects.get(user_email="tester@mail.com")._id),
                    "restaurant_id": "111111111111111111111111", "user_email": "tester@mail.com",
                    "price": "0", "is_cancelled": False, "send_tstmp": None, 'num_items': 0,
                    "accept_tstmp": None, "complete_tstmp": None}
        self.assertDictEqual(actual, expected)

    def test_insert_item_cart(self):
        """ Test if the cart price was updated after item insert """

        req = self.factory.post('/api/order/item/insert/', {'cart_id': str(self.c1._id), 'food_id': str(self.f1._id),
                                                            'count': 2},
                                content_type='application/json')
        view_response.insert_item_page(req)
        actual = Cart.objects.get(_id=self.c1._id).price
        expected = "21.98"
        self.assertEqual(actual, expected)

    def test_insert_item_item(self):
        """ Test if item document is inserted into the database """

        req = self.factory.post('/api/order/item/insert/', {'cart_id': str(self.c1._id), 'food_id': str(self.f1._id),
                                                            'count': 2},
                                content_type='application/json')
        actual = json.loads(view_response.insert_item_page(req).content)
        expected = {"_id": str(Item.objects.get(cart_id=str(self.c1._id), food_id= str(self.f1._id))._id),
                    "cart_id": str(self.c1._id), "food_id": str(self.f1._id), "count": 2}
        self.assertDictEqual(actual, expected)

    def test_get_items_by_cart(self):
        req = self.factory.get('api/order/item/get_by_cart/', {'cart_id': str(self.c1._id)}, content_type='application/json')
        actual = json.loads(view_response.get_items_by_cart_page(req).content)
        expected = {'items': [json.loads(json.dumps(model_to_dict(self.i), cls=BSONEncoder))]}
        self.assertDictEqual(actual, expected)

class CartStatusCases(TestCase):

    def setUp(self):
        """setup objects and constants"""
        # setup time
        self.time = datetime(2013, 4, 16, 12, 28, 52, 797923, pytz.UTC)
        self.time_str = '2013-04-16T12:28:52.797Z'

        self.cart1 = Cart.objects.create(**{
            "restaurant_id": "111111111111111111111111", "user_email": "tester@mail.com",
            "price": "0.00", "is_cancelled": False, "send_tstmp": None,
            "accept_tstmp": None, "complete_tstmp": None}
                                         )
        self.cart2 = Cart.objects.create(**{
            "restaurant_id": "111111111111111111311111", "user_email": "tester@mail.com",
            "price": "0.00", "is_cancelled": False, "send_tstmp": self.time,
            "accept_tstmp": None, "complete_tstmp": None}
                                         )
        self.cart3 = Cart.objects.create(**{
            "restaurant_id": "111111111111111111411111", "user_email": "tester@mail.com",
            "price": "0.00", "is_cancelled": False, "send_tstmp": self.time,
            "accept_tstmp": self.time, "complete_tstmp": None}
                                         )
        self.factory = RequestFactory()

    def test_send(self):
        """Test if send timestamp is updated"""
        request = self.factory.post('api/order/cart/update_status/', {
            '_id': str(self.cart1._id),
            'status': 'snd'
        }, content_type='application/json')

        time = self.time

        # mock class for datetime
        class mockdate:  # mock datetime
            def now(self):
                return time

        # setup mock
        mock = MockModule(models.timezone, mockdate())
        models.timezone = mock.mock()

        # setup actual, expected with mocked views
        response = view_response.update_status_page(request)
        actual = json.loads(response.content)
        expected = json.loads(json.dumps(model_to_dict(self.cart1), cls=BSONEncoder))
        expected['send_tstmp'] = self.time_str

        # undo
        models.timezone = mock.undo()

        self.assertDictEqual(expected, actual)

    def test_accept(self):
        """Test if accept timestamp is updated"""
        request = self.factory.post('api/order/cart/update_status/', {
            '_id': str(self.cart2._id),
            'status': 'acc'
        }, content_type='application/json')

        time = self.time

        # mock class for datetime
        class mockdate:  # mock datetime
            def now(self):
                return time

        # setup mock
        mock = MockModule(models.timezone, mockdate())
        models.timezone = mock.mock()

        # setup actual, expected with mocked views
        response = view_response.update_status_page(request)
        actual = json.loads(response.content)
        expected = json.loads(json.dumps(model_to_dict(self.cart2), cls=BSONEncoder))
        expected['accept_tstmp'] = self.time_str

        # undo
        models.timezone = mock.undo()

        self.assertDictEqual(expected, actual)


    def test_complete(self):
        """Test is complete timestamp is updated"""
        request = self.factory.post('api/order/cart/update_status/', {
            '_id': str(self.cart3._id),
            'status': 'cmt'
        }, content_type='application/json')

        time = self.time

        # mock class for datetime
        class mockdate:  # mock datetime
            def now(self):
                return time

        # setup mock
        mock = MockModule(models.timezone, mockdate())
        models.timezone = mock.mock()

        # setup actual, expected with mocked views
        response = view_response.update_status_page(request)
        actual = json.loads(response.content)
        expected = json.loads(json.dumps(model_to_dict(self.cart3), cls=BSONEncoder))
        expected['complete_tstmp'] = self.time_str

        # undo
        models.timezone = mock.undo()

        self.assertDictEqual(expected, actual)


    def test_order_fail(self):
        """Test is appropriate error response is sent upon invalid order"""
        request = self.factory.post('api/order/cart/update_status/', {
            '_id': str(self.cart1._id),
            'status': 'cmt'
        }, content_type='application/json')

        actual = view_response.update_status_page(request).content.decode("utf-8")
        self.assertEqual(str(actual), 'Could not complete order')

    def test_invalid_form(self):
        """Test if appropriate error response is sent upon invalid status"""
        request = self.factory.post('api/order/cart/update_status/', {
            '_id': str(self.cart1._id),
            'status': 'cmweft'
        }, content_type='application/json')

        actual = view_response.update_status_page(request).content.decode("utf-8")
        self.assertEqual(str(actual), 'Invalid request, please use check your request')

class CartRemoveTestCases(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.f1 = Food.objects.create(name="foodA", restaurant_id='mock',
                                description="chicken", picture="picA",
                                price='10.00')
        self.c1 = Cart.objects.create(restaurant_id='222222222222222222222222', user_email='test2@mail.com',
                                      price="100.00", num_items=1)
        self.c2 = Cart.objects.create(restaurant_id='222222222422222222222222', user_email='tes42@mail.com',
                                      price="100.00", num_items=2)
        self.c3 = Cart.objects.create(restaurant_id='222222222322222222222222', user_email= 'test3@mail.com',
                                      price="30.00", num_items=1)

        self.o = Item.objects.create(cart_id=self.c1._id, food_id=self.f1._id, count=2)
        self.o2 = Item.objects.create(cart_id=self.c2._id, food_id=self.f1._id, count=2)
        self.o3 = Item.objects.create(cart_id=self.c3._id, food_id=self.f1._id, count=3)

    def test_remove_cart(self):
        """Test if cart has been removed from the database"""
        request = self.factory.post('/api/order/item/remove/',
                                    {'item_id': str(self.o._id)}, content_type='application/json')
        view_response.remove_item_page(request)
        self.assertRaises(ObjectDoesNotExist, Cart.objects.get, _id=self.c1._id)

    def test_remove_item(self):
        """Test if item has been removed form database"""
        request = self.factory.post('/api/order/item/remove/',
                                    {'item_id': str(self.o._id)}, content_type='application/json')
        view_response.remove_item_page(request)
        self.assertRaises(ObjectDoesNotExist, Item.objects.get, _id=self.o._id)

    def test_remove_item_price(self):
        """Test is price and number of items is correctly decremented"""
        request = self.factory.post('/api/order/item/remove/',
                                    {'item_id': str(self.o2._id)}, content_type='application/json')
        view_response.remove_item_page(request)
        self.c2.refresh_from_db()
        expected, actual = model_to_dict(self.c2), model_to_dict(self.c2)
        expected['price'] = '80.00'
        expected['num_items'] = 1
        self.assertDictEqual(expected,actual)

    def test_item_count_change(self):
        """Test if an item has its count modified properly"""
        request = self.factory.post('/api/order/item/edit_amount/',
                                    {'item_id' : str(self.o3._id), 'count' : 2},  content_type='application/json')
        view_response.edit_item_amount_page(request)
        self.o3.refresh_from_db()
        expected, actual = model_to_dict(self.o3), model_to_dict(self.o3)
        expected['count'] = 2
        self.assertDictEqual(expected, actual)

    def test_count_change_cart_price(self):
        """test if editing the count of an item properly modifies cart price"""
        request = self.factory.post('/api/order/item/edit_amount/',
                                    {'item_id' : str(self.o3._id), 'count' : 1},  content_type='application/json')
        view_response.edit_item_amount_page(request)
        self.c3.refresh_from_db()
        expected, actual = model_to_dict(self.c3), model_to_dict(self.c3)
        expected['price'] = '10.00'
        self.assertDictEqual(expected, actual)

    def test_zerocount_deletion(self):
        """Test if an item is deleted when its count is modified to 0"""
        request = self.factory.post('/api/order/item/edit_amount/',
                                    {'item_id' : str(self.o3._id), 'count' : 0},  content_type='application/json')
        view_response.edit_item_amount_page(request)
        self.assertRaises(ObjectDoesNotExist, Item.objects.get, _id= self.o3._id)
