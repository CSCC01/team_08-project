from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from order.models import Cart, Item
from django.forms.models import model_to_dict
from jsonschema import validate
import json
from utils.encoder import BSONEncoder
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
            try:
                cart = getattr(Cart, status.value)(Cart, body['_id'])
                return JsonResponse(json.loads(json.dumps(model_to_dict(cart), cls=BSONEncoder)))
            except ValueError as error:
                return HttpResponseBadRequest(str(error))
    return HttpResponseBadRequest('Invalid request, please check your request')

def decline_cart_page(request):
    """Decline a cart which has been sent by a user"""
    validate(instance=request.body, schema=cart_schema)
    body = json.loads(request.body)
    try:
        cart = Cart.decline_cart(Cart, cart_id= body['_id'])
        return JsonResponse(json.loads(json.dumps(model_to_dict(cart), cls=BSONEncoder)))
    except ValueError as error:
        return HttpResponseBadRequest(str(error))
    return HttpResponseBadRequest('Invalid request, please check your request')


def insert_item_page(request):
    """ Insert item to database """
    validate(instance=request.body, schema=item_schema)
    body = json.loads(request.body)
    item = Item.new_item(body['cart_id'], body['food_id'], body['count'])
    item._id = str(item._id)
    return JsonResponse(model_to_dict(item))

def remove_item_page(request):
    """Insert Item to database"""
    validate(instance=request.body, schema=item_schema_remove)
    body = json.loads(request.body)
    Item.remove_item(body['item_id'])
    return HttpResponse('success')

def edit_item_amount_page(request):
    """Edit food item"""
    validate(instance= request.body, schema=item_schema)
    body = json.loads(request.body)
    responsemessage = Item.edit_item_amount(body['item_id'], body['count'])
    for entry in responsemessage:
        if not type(responsemessage[entry]) == dict:
            responsemessage[entry] = model_to_dict(responsemessage[entry])
    return JsonResponse(json.loads(json.dumps(responsemessage, cls=BSONEncoder)))
