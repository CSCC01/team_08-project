from djongo import models
from bson import ObjectId
from RO.models import Restaurant
from restaurant.models import Food
from auth2.models import SDUser


# Model for a restaurant review
class RestaurantReview(models.Model):
    _id = models.ObjectIdField()
    restaurant = models.ForeignKey(Restaurant)
    user = models.ForeignKey(SDUser)
    rating = models.IntegerField(default = 0)
    content = models.CharacterField(max_length = 3000)
    Timestamp = models.DateTimeField()