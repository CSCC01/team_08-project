from django.forms import model_to_dict
from djongo import models
from bson import ObjectId
from restaurant.cuisine_dict import load_dict
from cloud_storage import cloud_controller

# Model for the Food Items on the Menu
class Food(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=50, default='')
    restaurant_id = models.CharField(max_length=24, editable=False)
    description = models.CharField(max_length=200, blank=True, default='')
    picture = models.CharField(max_length=200, blank=True, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    tags = models.ListField(default=[], blank=True)
    specials = models.CharField(max_length=51, blank=True)

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
        )
        dish.clean_fields()
        dish.clean()
        dish.save()
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


# Model for Manual Tags
class ManualTag(models.Model):
    _id = models.ObjectIdField()
    category = models.CharField(max_length=20, choices=[  # Use enum later
        ("promo", "promo"),
        ("allergy", "allergy"),
        ('cuisine', 'cuisine'),
        ('dish', 'dish')
    ])
    value = models.CharField(max_length=50)
    foods = models.ListField(default=[], blank=True)



    # Clears all the tags off a food item
    @classmethod
    def clear_food_tags(cls, food_name, restaurant):  # To be changed when restaurant is implemented
        """
        Destroy all food -tag relationships for food
        :param food_name: name of food
        :param restaurant: id of restaurant
        :return: None
        """
        food = Food.objects.get(name=food_name,
                                restaurant_id=restaurant)  # To be changed when restaurant is implemented
        for tag_id in food.tags:
            tag = ManualTag.objects.get(_id=tag_id)
            for food_id in tag.foods:
                if food_id == food._id:
                    tag.foods.remove(food_id)
                    tag.save()
        food.tags = []
        food.save()

    # Adds Tag to food
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
        return [cls.add_tag(dish.name, dish.restaurant_id, 'dish', item)  # fancy list comprehension
                for item in desc_set.intersection(load_dict.read('dishes.csv'))]

    def __eq__(self, other):
        return self.food == other.food and self.category == other.category and self.value == other.value

class Restaurant(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    phone = models.BigIntegerField(null=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=40)
    cuisine = models.CharField(max_length=30)
    pricepoint = models.CharField(max_length=30)  # add choices, make enum
    twitter = models.CharField(max_length=200)
    instagram = models.CharField(max_length=200)
    bio = models.TextField(null=True)
    GEO_location = models.CharField(max_length=200)
    external_delivery_link = models.CharField(max_length=200)
    cover_photo_url = models.CharField(max_length=200, default='https://www.nautilusplus.com/content/uploads/2016/08/Pexel_junk-food.jpeg')
    logo_url = models.CharField(max_length=200, default='https://d1csarkz8obe9u.cloudfront.net/posterpreviews/diner-restaurant-logo-design-template-0899ae0c7e72cded1c0abc4fe2d76ae4_screen.jpg?ts=1561476509')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    @classmethod
    def get(cls, _id):
        """
        retrieve restaurant based on id
        :param _id: id of restaurant
        :return: restaurant json
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
        restaurant = cls(
            **restaurant_data
        )
        restaurant.clean_fields()
        restaurant.clean()
        restaurant.save()
        return restaurant

    @classmethod
    def update_logo(cls, img, _id):
        """
        Upload image to google cloud and change restaurant logo to that link
        :param img:
        :param _id:
        :return:
        """
        restaurant = cls.get(_id=_id)
        url = cloud_controller.upload(img, cloud_controller.TEST_BUCKET, content_type='image/png')
        restaurant.logo_url = url
        restaurant.save()
        return url



