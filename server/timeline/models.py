from djongo import models


# Model for a post on an restaurant's timeline
class TimelinePost(models.Model):
    _id = models.ObjectIdField()
    restaurant_id = models.CharField(max_length=24)
    user_email = models.EmailField()
    likes = models.ListField(default=[], blank=True)
    content = models.TextField(max_length=4096)
    Timestamp = models.DateTimeField(auto_now=True)
    comments = models.ListField(default=[], blank=True)

    @classmethod
    def get_by_restaurant(cls, rest_id):
        """
        Retrieve posts by restaurant id
        :param rest_id: id of restaurant
        :return: post data in json
        """
        return list(TimelinePost.objects.filter(restaurant_id=rest_id))

    @classmethod
    def get_all(cls):
        """
        retrieve list of posts from database
        :return: return list of posts json data wrapped in
        """
        return list(TimelinePost.objects.all())


# Model for a comment on a timeline post
class TimelineComment(models.Model):
    _id = models.ObjectIdField()
    post_id = models.CharField(max_length=24)
    user_email = models.EmailField()
    likes = models.ListField(default=[], blank=True)
    content = models.TextField(max_length=256)
    Timestamp = models.DateTimeField(auto_now=True)
