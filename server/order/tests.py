from django.test import TestCase, RequestFactory
from order.models import Cart, Item
from restaurant.models import Food
import order.views as view_response
import json
from django.forms import model_to_dict
from utils.encoder import BSONEncoder
from django.core.exceptions import ObjectDoesNotExist


class CartTestCases(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.c1 = Cart.objects.create(restaurant_id='222222222222222222222222', user_email='test2@mail.com', price=0)
        self.f1 = Food.objects.create(name="foodA", restaurant_id='mock',
                                      description="chicken", picture="picA",
                                      price='10.99')

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
        expected = {"_id": str(Item.objects.get(cart_id=str(self.c1._id))._id),
                    "cart_id": str(self.c1._id), "food_id": str(self.f1._id), "count": 2}
        self.assertDictEqual(actual, expected)


class CartSingleTestCases(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.c1 = Cart.objects.create(restaurant_id='222222222222222222222222', user_email='test2@mail.com',
                                      price="100.00", num_items=1)
        self.c2 = Cart.objects.create(restaurant_id='2222222224222222222222222', user_email='tes42@mail.com',
                                      price="100.00", num_items=2)
        self.f1 = Food.objects.create(name="foodA", restaurant_id='mock',
                                      description="chicken", picture="picA",
                                      price='10.00')
        self.o = Item.objects.create(cart_id=self.c1._id, food_id=self.f1._id, count=2)
        self.o2 = Item.objects.create(cart_id=self.c2._id, food_id=self.f1._id, count=2)

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


