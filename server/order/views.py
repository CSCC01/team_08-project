from bson import ObjectId
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from order.models import Cart, Item
from jsonschema import validate
import json
from .order_state import OrderStates
from django.core.exceptions import ObjectDoesNotExist
from utils.model_util import model_to_json

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


def get_restaurant_carts_page(request):
    """
    Gets the list of carts which have been sent, and are not completed, with this restaurant_id
    """
    restaurant_id = request.GET.get('restaurant_id')
    carts = Cart.restaurants_carts(Cart, restaurant_id)
    carts_dict = {'carts': []}
    for cart in carts:
        carts_dict['carts'].append(model_to_json(cart))
    return JsonResponse(carts_dict)


def get_users_cart_page(request):
    """
    Gets the user's active cart based on the given user_id,
    if 'is_sent' is 'true', give all sent carts
    otherwise give the only existing active cart
    """
    try:
        user_id = request.GET.get('user_email')
        if is_sent(request.GET.get('is_sent')):
            carts = Cart().users_sent_carts(user_id)
            carts_dict = {'carts': []}
            for cart in carts:  # serialize carts
                carts_dict['carts'].append(model_to_json(cart))
            return JsonResponse(carts_dict)
        else:
            cart = Cart().users_active_cart(user_id)
            return JsonResponse({'carts': [model_to_json(cart)]})
    except ObjectDoesNotExist:  # something went wrong (invalid user/no cart)
        return JsonResponse({'NoCart': 'Closed'})


def is_sent(sent):
    """
    check if cart is sent
    @param sent: param for checking if sent
    @return: boolean
    """
    # annoying workaround since the request param is a string
    # if sent.lower() == the string 'true' then it is true otherwise false
    return sent.lower() == 'true'


def insert_cart_page(request):
    """ Insert cart to database """
    validate(instance=request.body, schema=cart_schema)
    body = json.loads(request.body)
    cart = Cart.new_cart(body['restaurant_id'], body['user_email'])
    return JsonResponse(model_to_json(cart))


def update_status_page(request):
    """ Update cart status in database """
    validate(instance=request.body, schema=status_schema)
    body = json.loads(request.body)
    if valid_status(body['status']):
        try:
            cart = getattr(Cart, OrderStates[body['status']].value)(Cart, body['_id'])
            return JsonResponse(model_to_json(cart))
        except ValueError as error:
            return HttpResponseBadRequest(str(error))
    return HttpResponseBadRequest('Invalid request, please check your request')


def valid_status(status):
    """
    check whether status is valid
    @param status: status to be checked
    @return: boolean
    """
    return status in OrderStates.__members__


def decline_cart_page(request):
    """Decline a cart which has been sent by a user"""
    validate(instance=request.body, schema=cart_schema)
    body = json.loads(request.body)
    try:
        cart = Cart().decline_cart(cart_id=body['_id'])
        return JsonResponse(model_to_json(cart))
    except ValueError as error:
        return HttpResponseBadRequest(str(error))


def insert_item_page(request):
    """ Insert item to database """
    validate(instance=request.body, schema=item_schema)
    body = json.loads(request.body)
    item = Item.new_item(body['cart_id'], body['food_id'], body['count'])
    return JsonResponse(model_to_json(item))


def remove_item_page(request):
    """ Remove Item from database """
    validate(instance=request.body, schema=item_schema_remove)
    body = json.loads(request.body)
    Item.remove_item(body['item_id'])
    return HttpResponse('success')


def edit_item_amount_page(request):
    """ Edit food item """
    validate(instance=request.body, schema=item_schema)
    body = json.loads(request.body)
    responsemessage = Item.edit_item_amount(body['item_id'], body['count'])
    for entry in responsemessage:
        try:
            responsemessage[entry] = model_to_json(responsemessage[entry])
        except AttributeError:
            pass
    return JsonResponse(responsemessage)


def get_items_by_cart_page(request):
    """Get all items associated with a given cart"""
    items = Item.get_items_by_cart(request.GET['cart_id'])
    items = [model_to_json(item) for item in items]
    return JsonResponse({'items': items})


def cancel_cart_page(request):
    """ Deletes cart and all items in cart """
    validate(instance=request.body, schema=cart_schema)
    body = json.loads(request.body)
    cart = Cart.objects.get(_id=ObjectId(body['_id']))
    cart.cancel_cart()
    return HttpResponse('success')
