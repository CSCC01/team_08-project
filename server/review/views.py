import json

from bson import ObjectId
from django.http import JsonResponse

from restaurant.models import Restaurant
from review.models import Review
from jsonschema import validate

review_schema = {
    'properties': {
        'restaurant_id': {'type': 'string'},
        'user_email': {'type': 'string'},
        'title': {'type': 'string'},
        'content': {'type': 'string'},
        'rating': {'type': 'number'}
    }
}


def insert_review_page(request):
    """ Insert comment into database """
    validate(instance=request.body, schema=review_schema)
    body = json.loads(request.body)
    restaurant = Restaurant.objects.get(_id=ObjectId(body['restaurant_id']))
    review = Review.new_review(body)
    restaurant.rating = Review.new_rating(restaurant._id)
    restaurant.save(update_fields=['rating'])
    return JsonResponse({'_id': str(review._id), 'restaurant_id': review.restaurant_id, 'user_email': review.user_email,
                         'title': review.title, 'content': review.content,
                         'Timestamp': review.Timestamp.strftime("%b %d, %Y %H:%M"),
                         'rating': review.rating})


def get_restaurant_reviews_page(request):
    """ Get list of reviews from a restaurant from the database """
    return JsonResponse(Review.get_by_restaurant(request.GET.get('restaurant_id')))
