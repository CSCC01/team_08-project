from djongo import models


class Review(models.Model):
    _id = models.ObjectIdField()
    restaurant_id = models.CharField(max_length=24)
    user_email = models.EmailField()
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=4096)
    Timestamp = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(blank=True)

    @classmethod
    def new_review(cls, review_data):
        """
        Create new review and save to database
        :param review_data: data of new review
        :return: newly created review instance
        """
        review = cls(**review_data)
        review.clean_fields()
        review.clean()
        review.save()
        return review
