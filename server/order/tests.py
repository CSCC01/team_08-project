from django.test import TestCase, RequestFactory
from order.models import Cart
import order.views as view_response
import json
from utils.encoder import BSONEncoder
import datetime
import copy


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
        self.cart1 = Cart.objects.create({
            "restaurant_id": "111111111111111111111111", "user_email": "tester@mail.com",
            "price": "0.00", "is_cancelled": False, "send_tstmp": None,
            "accept_tstmp": None, "complete_tstmp": None}
        )
        self.cart2 = Cart.objects.create({
            "restaurant_id": "111111111111111111311111", "user_email": "tester@mail.com",
            "price": "0.00", "is_cancelled": False, "send_tstmp": datetime.datetime.now(),
            "accept_tstmp": None, "complete_tstmp": None}
        )
        self.cart3 = Cart.objects.create({
            "restaurant_id": "111111111111111111411111", "user_email": "tester@mail.com",
            "price": "0.00", "is_cancelled": False, "send_tstmp": datetime.datetime.now(),
            "accept_tstmp": datetime.datetime.now(), "complete_tstmp": None}
        )
        self.factory = RequestFactory()

    def test_send(self):
        request = self.factory.post('api/order/cart/update_status/', {
            '_id': str(self.cart._id),
            'status': 'snd'
        })
        # mock test datetime
        expected_time = datetime.datetime.now()
        class mockdate: # mock datetime
            class datetime:
                def now(self):
                    return expected_time

        mock_view = copy.deepcopy(view_response)
        mock_view.datetime = mockdate()



        actual = json.loads(json.dumps(mock_view.update_status_page(request), cls=BSONEncoder))
