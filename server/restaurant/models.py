from djongo import models
from bson import ObjectId
from restaurant.cuisine_dict import load_dict
from restaurant.enum import Prices, Categories
from django.core.exceptions import ObjectDoesNotExist
import requests
from utils.model_util import save_and_clean, update_model_geo
from geo.geo_controller import geocode

FOOD_PICTURE = 'https://storage.googleapis.com/default-assets/no-image.png'

RESTAURANT_COVER = 'https://storage.googleapis.com/default-assets/cover.jpg'
RESTAURANT_LOGO = 'https://storage.googleapis.com/default-assets/logo.jpg'
DISHES = 'dishes.csv'


class Food(models.Model):
    """ Model for the Food Items on the Menu """
    _id = models.ObjectIdField()
    name = models.CharField(max_length=50, default='')
    restaurant_id = models.CharField(max_length=24, editable=False)
    description = models.CharField(max_length=200, blank=True, default='')
    picture = models.CharField(max_length=200, blank=True,
                               default=FOOD_PICTURE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    tags = models.ListField(default=[], blank=True)
    specials = models.CharField(max_length=51, blank=True)
    category = models.CharField(max_length=50, blank=True, default='')

    class Meta:
        unique_together = (("name", "restaurant_id"),)

    def is_tagged(self, tag):
        """
        check if food is tagged with tag 'tag'
        @param tag: referenced tag
        @return: boolean
        """
        return tag._id in self.tags

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
            price=food_data['price'],
            specials=food_data['specials'],
            category=food_data['category'],
        )
        save_and_clean(dish)
        restaurant = Restaurant.objects.get(_id=food_data['restaurant_id'])
        if not restaurant.category_exists(food_data['category']):
            restaurant.categories.append(food_data['category'])
            restaurant.save(update_fields=['categories'])
        return dish


    @classmethod
    def get_by_restaurant(cls, rest_id):
        """
        Retrieve restaurant by id
        :param rest_id: id of restaurant
        :return: restaurant data in json
        """
        return list(Food.objects.filter(restaurant_id=rest_id))

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
                except (requests.ConnectionError, requests.exceptions.MissingSchema):
                    invalid['Invalid'].append(field)

        if not invalid['Invalid']:
            return None
        else:
            return invalid

    def clean_description(self):
        description = {food for food in self.description.split(' ')}
        clean_description = set()
        for word in description:  # clean word, remove non alphabetical
            clean_description.add(''.join(e for e in word if e.isalpha()))
        clean_description = set(map(str.lower, clean_description))
        return clean_description


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
            tag.remove_food(food._id)
        food.tags = []
        food.save()

    def remove_food(self, food_id):
        """
        remove food_id from tag
        @param food_id: referenced food_id
        """
        self.foods.remove(food_id)
        self.save()

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
        if not ManualTag.tag_exists(value, category):
            tag = cls(value=value, category=category, foods=[food._id])
            save_and_clean(tag)
            return tag

        tag = ManualTag.objects.get(value=value, category=category)
        if not food.is_tagged(tag):
            add_new_tag(food, tag)
        return tag

    @classmethod
    def tag_exists(cls, value, category):
        return cls.objects.filter(value=value, category=category).exists()

    @classmethod
    def auto_tag_food(cls, _id):
        """
        generate tags based on food description
        :param _id: id of food
        :return: list of generated tags
        """
        dish = Food.objects.get(_id=ObjectId(_id))
        clean_description = dish.clean_description()
        cuisine_dict = load_dict.read(DISHES)
        keywords = clean_description.intersection(cuisine_dict)
        tags = ManualTag().tag_description(keywords, dish)
        return tags

    def __eq__(self, other):
        return self.food == other.food and self.category == other.category and self.value == other.value


    @classmethod
    def tag_description(cls, keywords, dish):
        tags = []
        for keyword in keywords:
            tags.append(cls.add_tag(dish.name, dish.restaurant_id, Categories.DI.name, keyword))
        return tags


def add_new_tag(food, tag):
    """
    add new tag-food relationship
    @param food: food model
    @param tag: tag model
    """
    food.tags.append(tag._id)
    tag.foods.append(food._id)
    tag.save()
    food.save()


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
    GEO_location = models.CharField(max_length=200)
    external_delivery_link = models.CharField(max_length=200, blank=True)
    cover_photo_url = models.CharField(max_length=200,
                                       default='https://storage.googleapis.com/default-assets/cover.jpg')
    logo_url = models.CharField(max_length=200,
                                default='https://storage.googleapis.com/default-assets/logo.jpg')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    owner_name = models.CharField(max_length=50, blank=True)
    owner_story = models.CharField(max_length=3000, blank=True)
    owner_picture_url = models.CharField(max_length=200, blank=True)
    categories = models.ListField(default=[], blank=True)

    def category_exists(self, category):
        """
        Check whether category is new
        @param category: referenced category
        @return: boolean
        """
        return category in self.categories

    @classmethod
    def get(cls, _id):
        """
        retrieve restaurant based on id
        :param _id: id of restaurant
        :return: restaurant json or None
        """
        try:
            restaurant = Restaurant.objects.get(_id=_id)
            return restaurant
        except ObjectDoesNotExist:
            return None

    @classmethod
    def insert(cls, restaurant_data):
        """
        Insert restaurant into database given restaurant data
        :param restaurant_data: json data of restaurant
        :return: restaurant object representing sent data
        """
        try:
            cls.objects.get(email=restaurant_data['email'])
            raise ValueError('Cannot insert')
        except ObjectDoesNotExist:
            restaurant = cls(
                **restaurant_data
            )
            update_model_geo(restaurant, restaurant_data['address'])
            restaurant = save_and_clean(restaurant)
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
                except (requests.ConnectionError, requests.exceptions.MissingSchema):
                    invalid['Invalid'].append(field)

        if 'phone' in fields and fields['phone'] is not None:
            if len(str(fields['phone'])) != 10:
                invalid['Invalid'].append('phone')
        if 'address' in fields:
            try:
                geocode(fields['address'])
            except ValueError:
                invalid['Invalid'].append('address')
        if len(invalid['Invalid']) == 0:
            return None
        else:
            return invalid
