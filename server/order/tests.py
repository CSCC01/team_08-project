from django.test import TestCase, RequestFactory
from order.models import Cart
import order.views as view_response
import json
from utils.encoder import BSONEncoder
from django.forms import model_to_dict
from order import models
from datetime import datetime
import pytz
from utils.test_helper import MockModule
from django.http import HttpResponse


class CartTestCases(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_insert_cart(self):
        """ Test if cart document is inserted into the database """
        req = self.factory.post('/api/order/cart/insert/', {'restaurant_id': '111111111111111111111111',
                                                            'user_email': "tester@mail.com"},
                                content_type='application/json')
        actual = json.loads(view_response.insert_cart_page(req).content)
        expected = {"_id": str(Cart.objects.get(user_email="tester@mail.com")._id),
                    "restaurant_id": "111111111111111111111111", "user_email": "tester@mail.com",
                    "price": "0", "is_cancelled": False, "send_tstmp": None,
                    "accept_tstmp": None, "complete_tstmp": None}
        self.assertDictEqual(actual, expected)


class CartStatusCases(TestCase):

    def setUp(self):
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
        print(response)
        actual = json.loads(response.content)
        expected = json.loads(json.dumps(model_to_dict(self.cart2), cls=BSONEncoder))
        expected['accept_tstmp'] = self.time_str

        # undo
        models.timezone = mock.undo()

        self.assertDictEqual(expected, actual)


    def test_complete(self):
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
        print(response.content)
        actual = json.loads(response.content)
        expected = json.loads(json.dumps(model_to_dict(self.cart3), cls=BSONEncoder))
        expected['complete_tstmp'] = self.time_str

        # undo
        models.timezone = mock.undo()

        self.assertDictEqual(expected, actual)


    def test_order_fail(self):
        request = self.factory.post('api/order/cart/update_status/', {
            '_id': str(self.cart1._id),
            'status': 'cmt'
        }, content_type='application/json')

        actual = view_response.update_status_page(request).content.decode("utf-8")
        self.assertEqual(str(actual), 'Cannot update order status')

    def test_invalid_form(self):
        request = self.factory.post('api/order/cart/update_status/', {
            '_id': str(self.cart1._id),
            'status': 'cmweft'
        }, content_type='application/json')

        actual = view_response.update_status_page(request).content.decode("utf-8")
        self.assertEqual(str(actual), 'invalid request')