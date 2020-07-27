from djongo import models


# Model for a post on an restaurant's timeline
class TimelinePost(models.Model):
    _id = models.ObjectIdField()
    restaurant_id = models.CharField(max_length=24)
    user_id = models.CharField(max_length=24)
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
        response = {'Posts': []}
        for post in list(TimelinePost.objects.filter(restaurant_id=rest_id)):
            post._id = str(post._id)
            post.likes = list(map(str, post.likes))
            post.comments = list(map(str, post.comments))
            response['Posts'].append(({'_id': post._id, 'restaurant_id': post.restaurant_id, 'user_id': post.user_id,
                                       'content': post.content, 'likes': post.likes, 'comments': post.comments,
                                       'Timestamp': str(post.Timestamp)}))
        return response


# Model for a comment on a timeline post
class TimelineComment(models.Model):
    _id = models.ObjectIdField()
    post_id = models.CharField(max_length=24)
    user_id = models.CharField(max_length=24)
    likes = models.ListField(default=[], blank=True)
    content = models.TextField(max_length=256)
    Timestamp = models.DateTimeField(auto_now=True)
