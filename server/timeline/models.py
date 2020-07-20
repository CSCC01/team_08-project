from djongo import models
from bson import ObjectId
from RO.models import Restaurant
from restaurant.models import Food
from auth2.models import SDUser


# Model for a post on an restaurant's timeline
class TimelinePost(models.Model):
    _id = models.ObjectIdField()
    restaurant = models.ForeignKey(Restaurant)
    user = models.ForeignKey(SDUser)
    likes = models.IntegerField(default = 0)
    content = models.CharacterField(max_length = 3000)
    Timestamp = models.DateTimeField()

# Model for a comment on a timeline post
class TimelineComment(models.Model):
    _id = models.ObjectIdField()
    post = models.ForeignKey(TimelinePost)
    user = models.ForeignKey(SDUser)
    likes = models.IntegerField()
    content = models.CharField(max_length = 300)
    Timestamp = models.DateTimeField()
