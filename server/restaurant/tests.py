from django.core.exceptions import ValidationError
from django.test import TestCase
from restaurant.models import Food, ManualTag
from RO.models import Restaurant
from django.forms.models import model_to_dict


class TagTestCases(TestCase):

    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="RestA", address="123 Road", phone=None, email="RA@mail.com",
                                               city="Toronto",
                                               cuisine="Chinese", pricepoint="?", twitter="?", instagram="?", bio=None,
                                               GEO_location="?", external_delivery_link="?", cover_photo_url="picA",
                                               logo_url="urlA", rating="4.5")

        self.food = Food.objects.create(name="foodA", restaurant_id=str(self.restaurant._id), description="descripA", picture="picA",
                                   price=10.99)
        self.tag = ManualTag.objects.create(foods=[self.food._id], category="promo", value="50% off")
        self.food.tags = [self.tag._id]
        self.food.save()
        Food.objects.create(name="foodB", restaurant_id=self.restaurant._id, description="descripB", picture="picB",
                            price=20.99)


    def test_clear_food_tags_a(self):
        restaurant = Restaurant.objects.get(name="RestA")
        ManualTag.clear_food_tags(food_name="foodA", restaurant=restaurant._id)
        self.food.refresh_from_db()

        self.assertListEqual(self.food.tags, [])

    def test_clear_food_tags_b(self):
        restaurant = Restaurant.objects.get(name="RestA")
        ManualTag.clear_food_tags(food_name="foodA", restaurant=restaurant._id)
        self.tag.refresh_from_db()

        self.assertListEqual(self.tag.foods, [])


class AddTagCase(TestCase):
    def setUp(self):
        self.food = Food.objects.create(name="foodA", restaurant_id='mock',
                                        description="descripA", picture="picA",
                                        price=10.99)
        self.tag = ManualTag.objects.create(foods=[], category="promo", value="50% off")

    def test_add_tag_exist_a(self):
        ManualTag.add_tag(food_name='foodA', category='promo', restaurant='mock', value='50% off')
        self.tag.refresh_from_db()
        self.assertListEqual([self.food._id], self.tag.foods)

    def test_add_tag_exist_b(self):
        ManualTag.add_tag(food_name='foodA', category='promo', restaurant='mock', value='50% off')
        self.food.refresh_from_db()
        self.assertListEqual([self.tag._id], self.food.tags)

    def test_add_tag_dne_a(self):
        ManualTag.add_tag(food_name='foodA', category='promo', restaurant='mock', value='30% off')
        self.tag = ManualTag.objects.get(value='30% off', category='promo')
        self.assertListEqual([self.food._id], self.tag.foods)

    def test_add_tag_tagged_a(self):
        self.tag.foods = [self.food._id]
        self.food.tags = [self.tag._id]
        self.food.save()
        self.tag.save()
        ManualTag.add_tag(food_name='foodA', category='promo', restaurant='mock', value='50% off')
        self.assertListEqual(self.tag.foods, [self.food._id])

    def test_add_tag_tagged_b(self):
        self.tag.foods = [self.food._id]
        self.food.tags = [self.tag._id]
        self.food.save()
        self.tag.save()
        ManualTag.add_tag(food_name='foodA', category='promo', restaurant='mock', value='50% off')
        self.assertListEqual(self.food.tags, [self.tag._id])

class AutoTag(TestCase):
    def setUp(self):
        self.food = Food.objects.create(name="foodA", restaurant_id='mock',
                                        description="chicken", picture="picA",
                                        price='10.99')

    def test_auto(self):
        actual = model_to_dict(ManualTag.auto_tag_food(self.food._id)[0])
        expected = model_to_dict(ManualTag.objects.get(category='dish', value='chicken'))
        expected['_id'] = str(expected['_id'])
        expected['foods'] = [str(food) for food in expected['foods']]
        self.assertDictEqual(expected,actual )

class FoodTestCases(TestCase):

    def setUp(self):
        self.foodA = Food.objects.create(name="foodA", restaurant_id="restA", description="descripA", picture="picA",
                                 price='10.99')
        self.foodB = Food.objects.create(name="foodB", restaurant_id="restB", description="descripB", picture="picB",
                            price='20.99')

    def test_get_all_foods(self):
        actual = Food.get_all()
        expected = {'Dishes': [model_to_dict(self.foodA), model_to_dict(self.foodB)]}
        expected['Dishes'][0]['_id'] = str(expected['Dishes'][0]['_id'])
        expected['Dishes'][1]['_id'] = str(expected['Dishes'][1]['_id'])
        self.assertDictEqual(expected, actual)
