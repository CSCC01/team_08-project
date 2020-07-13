from djongo import models
from bson import ObjectId
from RO.models import Restaurant
from restaurant.models import Food
from auth2.models import SDUser


# Model for a post on an restaurant's timeline
class SearchRecord(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey(SDUser)
    query = models.CharField(max_length = 50)
    querytype = models.CharField(max_length = 30)
    filters = models.ListField()
    Timestamp = models.DateTimeField()

# Model for a comment on a timeline post
class VisitRecord(models.Model):
    _id = models.ObjectIdField()
    visitid = models.ObjectIdField()
    visittype = models.CharField(max_length = 30)
    Timestamp = models.DateTimeField()
