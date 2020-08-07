from django.forms import model_to_dict
from djongo import models
from bson import ObjectId
from restaurant.cuisine_dict import load_dict
from cloud_storage import cloud_controller
from restaurant.enum import Prices, Categories
from django.core.exceptions import ObjectDoesNotExist
import requests
from geo import geo_controller

class Food(models.Model):
    """ Model for the Food Items on the Menu """
    _id = models.ObjectIdField()
    name = models.CharField(max_length=50, default='')
    restaurant_id = models.CharField(max_length=24, editable=False)
    description = models.CharField(max_length=200, blank=True, default='')
    picture = models.CharField(max_length=200, blank=True, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    tags = models.ListField(default=[], blank=True)
    specials = models.CharField(max_length=51, blank=True)
    category = models.CharField(max_length=50, blank=True, default='')

    class Meta:
        unique_together = (("name", "restaurant_id"),)

    @classmethod
    def add_dish(cls, food_data):
        """
        insert dish into database and return response
        :param food_data: dictionary representation of dish
        :return: Food model object
        """
        dish = cls(
            name=food_data['name'],
            restaurant_id=food_data['restaurant_id'],
            description=food_data['description'],
            picture=food_data['picture'],
            price=food_data['price'],
            specials=food_data['specials'],
            category=food_data['category'],
        )
        dish.clean_fields()
        dish.clean()
        dish.save()
        restaurant = Restaurant.objects.get(_id=food_data['restaurant_id'])
        if food_data['category'] not in restaurant.categories:
            restaurant.categories.append(food_data['category'])
            restaurant.save(update_fields=['categories'])
        return Food.objects.get(name=food_data['name'], restaurant_id=food_data['restaurant_id'])

    @classmethod
    def get_all(cls):
        """
        retrieve list of restaurants from database
        :return: return list of restaurant json data wrapped in dictionary
        """
        response = {'Dishes': []}
        for food in list(Food.objects.all()):
            food._id = str(food._id)
            food.tags = list(map(str, food.tags))
            response['Dishes'].append(model_to_dict(food))
        return response

    @classmethod
    def get_by_restaurant(cls, rest_id):
        """
        Retrieve restaurant by id
        :param rest_id: id of restaurant
        :return: restaurant data in json
        """
        response = {'Dishes': []}
        for food in list(Food.objects.filter(restaurant_id=rest_id)):
            food._id = str(food._id)
            food.tags = list(map(str, food.tags))
            response['Dishes'].append(model_to_dict(food))
        return response

    @classmethod
    def field_validate(self, fields):
        """
        Validates fields
        :param fields: Dictionary of fields to validate
        :return: A list of fields that were invalid. Returns None if all fields are valid
        """
        dish_urls = ['picture']
        invalid = {'Invalid': []}

        for field in dish_urls:
            if field in fields and fields[field] != '':
                try:
                    requests.get(fields[field])
                except (requests.ConnectionError, requests.exceptions.MissingSchema) as exception:
                    invalid['Invalid'].append(field)

        if not invalid['Invalid']:
            return None
        else:
            return invalid


class ManualTag(models.Model):
    """ Model for Manual Tags """
    _id = models.ObjectIdField()
    category = models.CharField(max_length=4, choices=Categories.choices())
    value = models.CharField(max_length=50)
    foods = models.ListField(default=[], blank=True)

    @classmethod
    def clear_food_tags(cls, food_name, restaurant_id):
        """
        Destroy all food-tag relationships for food
        :param food_name: name of food
        :param restaurant: id of restaurant
        :return: None
        """
        food = Food.objects.get(name=food_name,
                                restaurant_id=restaurant_id)
        for tag_id in food.tags:
            tag = ManualTag.objects.get(_id=tag_id)
            for food_id in tag.foods:
                if food_id == food._id:
                    tag.foods.remove(food_id)
                    tag.save()
        food.tags = []
        food.save()

    @classmethod
    def add_tag(cls, food_name, restaurant_id, category, value):
        """
        Add tag to food
        :param food_name: name of food
        :param restaurant_id: id of restaurant
        :param category: category of following tag
        :param value: value of following tag
        :return: following tag object
        """
        food = Food.objects.get(name=food_name,
                                restaurant_id=restaurant_id)
        if not ManualTag.objects.filter(value=value, category=category).exists():
            tag = cls(value=value, category=category, foods=[])
            tag.clean_fields()
            tag.clean()
            tag.save()
        tag = ManualTag.objects.get(value=value, category=category)

        if tag._id not in food.tags:
            food.tags.append(tag._id)
            food.save()
            tag.foods.append(food._id)
            tag.save()
        tag._id = str(tag._id)
        tag.foods = [str(food) for food in tag.foods]
        return tag

    @classmethod
    def auto_tag_food(cls, _id):
        """
        generate tags based on food description
        :param _id: id of food
        :return: list of generated tags
        """
        dish = Food.objects.get(_id=ObjectId(_id))
        desc_set = {''.join(e for e in food if e.isalpha()).lower()
                    for food in dish.description.split(' ')}  # fancy set comprehension
        return [cls.add_tag(dish.name, dish.restaurant_id, 'DI', item)  # fancy list comprehension
                for item in desc_set.intersection(load_dict.read('dishes.csv'))]

    def __eq__(self, other):
        return self.food == other.food and self.category == other.category and self.value == other.value


class Restaurant(models.Model):
    """ Model for Restaurants """
    _id = models.ObjectIdField()
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    phone = models.BigIntegerField(null=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=40)
    cuisine = models.CharField(max_length=30)
    pricepoint = models.CharField(max_length=10, choices=Prices.choices())
    twitter = models.CharField(max_length=200, blank=True)
    instagram = models.CharField(max_length=200, blank=True)
    bio = models.TextField(null=True)
    GEO_location = models.CharField(blank=True, max_length=200)
    external_delivery_link = models.CharField(max_length=200, blank=True)
    cover_photo_url = models.CharField(max_length=200,
                                       default='https://www.nautilusplus.com/content/uploads/2016/08/Pexel_junk-food.jpeg')
    logo_url = models.CharField(max_length=200,
                                default='https://d1csarkz8obe9u.cloudfront.net/posterpreviews/diner-restaurant-logo-design-template-0899ae0c7e72cded1c0abc4fe2d76ae4_screen.jpg?ts=1561476509')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    owner_name = models.CharField(max_length=50, blank=True)
    owner_story = models.CharField(max_length=3000, blank=True)
    owner_picture_url = models.CharField(max_length=200, blank=True)
    categories = models.ListField(default=[], blank=True)

    @classmethod
    def get(cls, _id):
        """
        retrieve restaurant based on id
        :param _id: id of restaurant
        :return: restaurant json or None
        """
        restaurant = list(Restaurant.objects.filter(_id=ObjectId(_id)))
        if len(restaurant) == 1:
            restaurant[0]._id = str(restaurant[0]._id)
            return restaurant[0]
        return None

    @classmethod
    def get_all(cls):
        """
        Retrieve all restaurants from database
        :return: list of restauarant json wrapped in jsons
        """
        response = {'Restaurants': []}
        for restaurant in list(Restaurant.objects.all()):
            restaurant._id = str(restaurant._id)
            response['Restaurants'].append(model_to_dict(restaurant))
        return response

    @classmethod
    def insert(cls, restaurant_data):
        """
        Insert restaurant into database given restaurant data
        :param restaurant_data: json data of restaurant
        :return: restaurant object representing sent data
        """
        try:
            cls.objects.get(email=restaurant_data['email'])
            return None
        except ObjectDoesNotExist:
            restaurant = cls(
                **restaurant_data
            )
            try:
                restaurant.GEO_location = geo_controller.geocode(restaurant_data['address'])
            except ValueError:
                pass
            restaurant.clean_fields()
            restaurant.clean()
            restaurant.save()
            return restaurant

    @classmethod
    def field_validate(self, fields):
        """
        Validates fields
        :param fields: Dictionary of fields to validate
        :return: A list of fields that were invalid. Returns None if all fields are valid
        """
        restaurant_urls = ['twitter', 'instagram', 'cover_photo_url', 'logo_url', 'owner_picture_url',
                           'external_delivery_link']

        invalid = {'Invalid': []}

        for field in restaurant_urls:
            if field in fields and fields[field] != '':
                try:
                    requests.get(fields[field])
                except (requests.ConnectionError, requests.exceptions.MissingSchema) as exception:
                    invalid['Invalid'].append(field)

        if 'phone' in fields and fields['phone'] is not None:
            if len(str(fields['phone'])) != 10:
                invalid['Invalid'].append('phone')
        if len(invalid['Invalid']) == 0:
            return None
        else:
            return invalid
