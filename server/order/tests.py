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
                    "price": "0", "is_cancelled": False, "send_tstmp": None,
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


class CartRemoveTestCases(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.c1 = Cart.objects.create(restaurant_id='222222222222222222222222', user_email='test2@mail.com',
                                      price="100.00")
        self.f1 = Food.objects.create(name="foodA", restaurant_id='mock',
                                      description="chicken", picture="picA",
                                      price='10.00')
        self.o = Item.objects.create(cart_id=self.c1._id, food_id=self.f1._id, count=2)

    def test_remove_price(self):
        """Test is price is correctly changed"""
        request = self.factory.post('/api/order/item/remove/',
                                    {'item_id': str(self.o._id), 'count': 1}, content_type='application/json')
        cart = view_response.remove_item_page(request)
        actual = json.loads(cart.content)
        expected = json.loads(json.dumps(model_to_dict(self.c1), cls=BSONEncoder))
        expected['price'] = '90.00'
        self.assertDictEqual(actual, expected)

    def test_remove_item(self):
        """Test if item count is lowered"""
        request = self.factory.post('/api/order/item/remove/',
                                    {'item_id': str(self.o._id), 'count': 1}, content_type='application/json')
        view_response.remove_item_page(request)
        expected = json.loads(json.dumps(model_to_dict(self.o), cls=BSONEncoder))
        expected['count'] = 1
        self.o.refresh_from_db()
        actual = json.loads(json.dumps(model_to_dict(self.o), cls=BSONEncoder))
        self.assertDictEqual(actual, expected)

    def test_remove_price_over(self):
        """Test if price is not over charged"""
        request = self.factory.post('/api/order/item/remove/',
                                    {'item_id': str(self.o._id), 'count': 3}, content_type='application/json')
        cart = view_response.remove_item_page(request)
        actual = json.loads(cart.content)
        expected = json.loads(json.dumps(model_to_dict(self.c1), cls=BSONEncoder))
        expected['price'] = '80.00'
        self.assertDictEqual(actual, expected)

    def test_remove_item_delete(self):
        """Test if document has been removed form database"""
        request = self.factory.post('/api/order/item/remove/',
                                    {'item_id': str(self.o._id), 'count': 3}, content_type='application/json')
        view_response.remove_item_page(request)
        self.assertRaises(ObjectDoesNotExist, Item.objects.get, _id=self.o._id)
