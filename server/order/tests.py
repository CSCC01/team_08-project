from django.test import TestCase, RequestFactory
from order.models import Cart
import order.views as view_response
import json


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
