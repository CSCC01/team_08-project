from djongo import models
from django.forms.models import model_to_dict
from bson.objectid import ObjectId
from cloud_storage import cloud_controller

# Create your models here.

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
        restaurant = list(Restaurant.objects.filter(_id=ObjectId(_id)))
        if len(restaurant) == 1:
            restaurant[0]._id = str(restaurant[0]._id)
            return restaurant[0]
        return None

    @classmethod
    def update_logo(cls, img, _id):
        restaurant = cls.get(_id=_id)
        url = cloud_controller.upload(img, cloud_controller.TEST_BUCKET)
        restaurant.logo_url = url
        restaurant.save()
        return url

    @classmethod
    def get_all(cls):
        # TODO add delete
        response = {'Restaurants': []}
        for restaurant in list(Restaurant.objects.all()):
            restaurant._id = str(restaurant._id)
            response['Restaurants'].append(model_to_dict(restaurant))
        return response

    @classmethod
    def insert(cls, restaurant_data):
        restaurant = cls(
            **restaurant_data
        )
        restaurant.clean_fields()
        restaurant.clean()
        restaurant.save()
        return restaurant


