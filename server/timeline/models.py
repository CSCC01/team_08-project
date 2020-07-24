from djongo import models
from bson import ObjectId
from restaurant.models import Restaurant
from restaurant.models import Food
from auth2.models import SDUser


# Model for a post on an restaurant's timeline
class TimelinePost(models.Model):
    _id = models.ObjectIdField()
    restaurant_id = models.CharField(max_length=24)
    user_id = models.CharField(max_length=24)
    likes = models.ListField()
    content = models.CharacterField(max_length=3000)
    Timestamp = models.DateTimeField()
    comments = models.ListField()


# Model for a comment on a timeline post
class TimelineComment(models.Model):
    _id = models.ObjectIdField()
    post = models.ForeignKey(TimelinePost)
    user_id = models.CharField(max_length=24)
    likes = models.ListField()
    content = models.CharField(max_length=300)
    Timestamp = models.DateTimeField()
