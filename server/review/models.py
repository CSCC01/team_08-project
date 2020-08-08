from django.forms import model_to_dict
from djongo import models


class Review(models.Model):
    _id = models.ObjectIdField()
    restaurant_id = models.CharField(max_length=24)
    user_email = models.EmailField()
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=4096)
    Timestamp = models.DateTimeField(auto_now=True)
    rating = models.IntegerField()

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

    @classmethod
    def get_by_restaurant(cls, rest_id):
        """
        gets all reviews for a restaurant
        :param rest_id: the id of restaurant
        :return: a dictionary containing a list of reviews for a restaurant
        """
        response = {'Reviews': []}
        for review in list(Review.objects.filter(restaurant_id=rest_id)):
            review._id = str(review._id)
            response['Reviews'].append(
                {'_id': str(review._id), 'restaurant_id': review.restaurant_id, 'user_email': review.user_email,
                 'title': review.title, 'content': review.content,
                 'Timestamp': review.Timestamp.strftime("%b %d, %Y %H:%M"),
                 'rating': review.rating})
        return response

    @classmethod
    def new_rating(cls, rest_id):
        """
        calculates the rating of a restaurant based on restaurant reviews
        :param rest_id: the id of the restaurant
        :return: the average rating of the restaurant
        """
        total = 0
        reviews = list(Review.objects.filter(restaurant_id=rest_id))
        num_reviews = len(reviews)
        for review in reviews:
            total = review.rating + total
        return round(total / num_reviews, 2)
