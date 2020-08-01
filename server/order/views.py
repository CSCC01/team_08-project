from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from order.models import Cart, Item
from django.forms.models import model_to_dict
from jsonschema import validate
import json
from utils.encoder import BSONEncoder
from request_form import upload_form

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

item_schema = {
    "properties": {
        "_id": {"type": "string"},
        "cart_id": {"type": "string"},
        "food_id": {"type": "string"},
        "count": {"type": "number"},
    }
}

item_schema_remove = {
    'properties': {
        'item_id': {'type': 'string'},
        'count': {'type': 'integer'}
    }
}


def insert_cart_page(request):
    """ Insert cart to database """
    validate(instance=request.body, schema=cart_schema)
    body = json.loads(request.body)
    cart = Cart.new_cart(body['restaurant_id'], body['user_email'])
    cart._id = str(cart._id)
    return JsonResponse(model_to_dict(cart))


def insert_item_page(request):
    """ Insert item to database """
    validate(instance=request.body, schema=item_schema)
    body = json.loads(request.body)
    item = Item.new_item(body['cart_id'], body['food_id'], body['count'])
    item._id = str(item._id)
    return JsonResponse(model_to_dict(item))


def remove_item_page(request):
    """Insert Item to datbase"""
    validate(instance=request.body, schema=item_schema_remove)
    body = json.loads(request.body)
    cart = Item.remove_item(body['item_id'], body['count'])
    return JsonResponse(json.loads(json.dumps(model_to_dict(cart), cls=BSONEncoder)))
