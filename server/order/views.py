from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from order.models import Cart
from django.forms.models import model_to_dict
from jsonschema import validate
import json
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


def insert_cart_page(request):
    """ Insert cart to database """
    validate(instance=request.body, schema=cart_schema)
    body = json.loads(request.body)
    cart = Cart.new_cart(body['restaurant_id'], body['user_email'])
    cart._id = str(cart._id)
    return JsonResponse(model_to_dict(cart))
