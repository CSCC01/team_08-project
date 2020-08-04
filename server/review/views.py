import json
from django.http import JsonResponse
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
    review = Review.new_review(body)
    return JsonResponse({'_id': str(review._id), 'restaurant_id': review.restaurant_id, 'user_email': review.user_email,
                         'title': review.title, 'content': review.content,
                         'Timestamp': review.Timestamp.strftime("%b %d, %Y %H:%M"),
                         'rating': review.rating})


def get_restaurant_reviews_page(request):
    """ Get list of reviews from a restaurant from the database """
    return JsonResponse(Review.get_by_restaurant(request.GET.get('restaurant_id')))


