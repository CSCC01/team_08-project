from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from order.models import Cart
from django.forms.models import model_to_dict
from jsonschema import validate
import json
from request_form import upload_form
from utils.encoder import BSONEncoder
from .order_state import OrderStates

# jsonschema validation schemes
cart_schema = {
    "properties": {
        "_id": {"type": "string"},
        "restaurant_id": {"type": "string"},
        "user_email": {"type": "string"},
        "price": {"type": "string"},
        "is_cancelled": {"type": "boolean"},
    }
}

status_schema = {
    'properties': {
        '_id': {'type': 'string'},
        'status': {'type': 'string'}
    }
}


def insert_cart_page(request):
    """ Insert cart to database """
    validate(instance=request.body, schema=cart_schema)
    body = json.loads(request.body)
    cart = Cart.new_cart(body['restaurant_id'], body['user_email'])
    return JsonResponse(json.loads(json.dumps(model_to_dict(cart), cls=BSONEncoder)))


def update_status_page(request):
    """Update cart status in database"""
    validate(instance=request.body, schema=status_schema)
    body = json.loads(request.body)
    for status in OrderStates:
        if status.name == body['status']:
            cart = getattr(Cart, status.value)(Cart, body['_id'])
            if cart:
                return JsonResponse(json.loads(json.dumps(model_to_dict(cart), cls=BSONEncoder)))
            else:
                return HttpResponseBadRequest('Cannot update order status')
    return HttpResponseBadRequest('invalid request')