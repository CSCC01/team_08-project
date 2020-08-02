from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from user.models import SDUser
from restaurant.models import Restaurant
import json
from jsonschema import validate

# jsonschema validation scheme
signup_schema = {
    "properties": {
        "nickname": {"type": "string"},
        "name": {"type": "string"},
        "picture": {"type": "string"},
        "updated_at": {"type": "string"},
        "email": {"type": "string"},
        "email_verified": {"type": "boolean"},
        "role": {"type": "string"},
        "restaurant_id": {"type": "string"},
        "birthday": {"type": "string", "format": "date"},
        "address": {"type": "string"},
        "phone": {"type": "number"},
        "GEO_location": {"type": "string"}
    }
}

user_editable = ["nickname", "name", "picture", "updated_at", "birthday", "address", "phone", "GEO_location"]


def signup_page(request):
    """ Page to insert a user into the db provided all the user fields """
    validate(instance=request.body, schema=signup_schema)
    body = json.loads(request.body)
    user = SDUser.signup(nickname=body['nickname'], name=body['name'], picture=body['picture'],
                         updated=body['updated_at'], email=body['email'],
                         verified=body['email_verified'], role=body['role'], restaurant_id=body['restaurant_id'])
    return JsonResponse(model_to_dict(user))


def reassign_page(request):
    """
    Page to change the role of a user provided the user email and new role (If upgraded to RO must
    provide fields to make new restaurant instance
    """
    validate(instance=request.body, schema=signup_schema)
    body = json.loads(request.body)
    user = SDUser.objects.get(pk=body['user_email'])
    user.reassign_role(body['role'])
    if body['role'] == "RO":
        del body['user_email']
        del body['role']
        restaurant = Restaurant.insert(body)
        user.restaurant_id = str(restaurant._id)
        user.save(update_fields=["restaurant_id"])
        return JsonResponse({"restaurant_id": str(restaurant._id)})
    else:
        user.restaurant_id = None
        user.save(update_fields=["restaurant_id"])
    return HttpResponse(status=200)


def data_page(request):
    """ Page that returns all the user_data provided the user email """
    req_email = request.GET.get('email')
    user = SDUser.objects.get(pk=req_email)
    return JsonResponse(model_to_dict(user))


def exists_page(request):
    """ Page that checks if an email is already registered in the database provided an user email """
    req_email = request.GET.get('email')
    return JsonResponse({'exists': SDUser.objects.filter(email=req_email).exists()})


def edit_user_page(request):
    """Update User data"""
    validate(instance=request.body, schema=signup_schema)
    body = json.loads(request.body)
    invalid = SDUser.field_validate(body)
    if invalid is not None:
        return JsonResponse(invalid)
    user = SDUser.objects.get(email=body["email"])
    del body['email']
    for field in body:
        if field in user_editable:
            setattr(user, field, body[field])
    user.clean_fields()
    user.clean()
    user.save()
    return JsonResponse(model_to_dict(user))
