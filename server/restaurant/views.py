from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from restaurant.models import Food, ManualTag, Restaurant
from django.forms.models import model_to_dict
from jsonschema import validate
import json
from request_form import upload_form
from geo import geo_controller
# jsonschema validation schemes
from utils.model_json import model_to_json

food_schema = {
    "properties": {
        "_id": {"type": "string"},
        "name": {"type": "string"},
        "restaurant_id": {"type": "string"},
        "description": {"type": "string"},
        "picture": {"type": "string"},
        "price": {"type": "string"},
        "tags": {"type": "array",
                 "items": {"type": "string"}
                 },
        "specials": {"type": "string"},
    }
}

tag_schema = {
    "properties": {
        "_id": {"type": "string"},
        "value": {"type": "string"},
        "category": {"type": "string"},
        "foods": {"type": "array",
                  "items": {"type": "string"}
                  }
    }
}

restaurant_schema = {
    "properties": {
        "_id": {"type": "string"},
        "name": {"type": "string"},
        "address": {"type": "string"},
        "phone": {"type": "number"},
        "email": {"type": "string"},
        "city": {"type": "string"},
        "cuisine": {"type": "string"},
        "pricepoint": {"type": "string"},
        "twitter": {"type": "string"},
        "instagram": {"type": "string"},
        "bio": {"type": "string"},
        "GEO_location": {"type": "string"},
        "external_delivery_link": {"type": "string"},
        "cover_photo_url": {"type": "string"},
        "logo_url": {"type": "string"},
        "rating": {"type": "string"},
        "owner_name": {"type": "string"},
        "owner_story": {"type": "string"},
        "owner_picture_url": {"type": "string"}
    }
}

dish_editable = ["name", "description", "picture", "price", "specials", "category"]

restaurant_editable = ["name", "address", "phone", "updated_at", "email", "city", "cuisine", "pricepoint", "twitter",
                       "instagram", "bio", "external_delivery_link", "cover_photo_url", "logo_url",
                       "owner_name", "owner_story", "owner_picture_url"]


def insert_tag_page(request):
    """Insert tag to database"""
    validate(instance=request.body, schema=tag_schema)
    body = json.loads(request.body)
    tag = ManualTag.add_tag(body['food_name'], body['restaurant_id'], body['category'], body['value'])
    return JsonResponse(model_to_dict(tag))


def clear_tags_page(request):
    """Clear tags/food relationship"""
    validate(instance=request.body, schema=tag_schema)
    body = json.loads(request.body)
    ManualTag.clear_food_tags(body['food_name'], body['restaurant_id'])
    return HttpResponse(status=200)


def get_dish_by_restaurant_page(request):
    """Retrieve all dishes from a restaurant"""
    rest_id = request.GET.get('restaurant_id')
    return JsonResponse(Food.get_by_restaurant(rest_id))


def all_dishes_page(request):
    """Retrieve all dishes from the database"""
    return JsonResponse(Food.get_all())


def insert_dish_page(request):
    """Insert dish into database"""
    validate(instance=request.body, schema=food_schema)
    body = json.loads(request.body)
    invalid = Food.field_validate(body)
    if invalid is not None:
        return JsonResponse(invalid)
    food = Food.add_dish(body)
    food._id = str(food._id)
    return JsonResponse(model_to_dict(food))


def delete_dish_page(request):
    """ Deletes dish from database """
    validate(instance=request.body, schema=tag_schema)
    body = json.loads(request.body)
    ManualTag.clear_food_tags(body["food_name"], body["restaurant_id"])
    food = Food.objects.get(name=body["food_name"], restaurant_id=body["restaurant_id"])
    food.delete()
    if not Food.objects.filter(restaurant_id=body["restaurant_id"], category=food.category).exists():
        restaurant = Restaurant.objects.get(_id=body['restaurant_id'])
        restaurant.categories.remove(food.category)
        restaurant.save(update_fields=['categories'])
    return HttpResponse(status=200)


def auto_tag_page(request):
    """Automatically generate tags for food"""
    validate(instance=request.body, schema=food_schema)
    body = json.loads(request.body)
    tags = [model_to_dict(tag) for tag in ManualTag.auto_tag_food(body['_id'])]
    return JsonResponse({'tags': tags})


def get_restaurant_page(request):
    """retrieve restaurant by id"""
    _id = request.GET.get('_id')

    restaurant = Restaurant.get(_id)
    if restaurant:
        return JsonResponse(model_to_dict(restaurant))
    else:
        return JsonResponse({})


def get_all_restaurants_page(request):
    """Retrieve all restaurants"""
    return JsonResponse(Restaurant.get_all())


def insert_restaurant_page(request):
    """Insert new restaurant into database"""
    validate(instance=request.body, schema=restaurant_schema)
    body = json.loads(request.body)
    invalid = Restaurant.field_validate(body)
    if invalid is not None:
        return JsonResponse(invalid)
    restaurant = Restaurant.insert(body)
    if restaurant is not None:
        restaurant._id = str(restaurant._id)
        return JsonResponse(model_to_dict(restaurant))
    else:
        return HttpResponseBadRequest('duplicate email')


def edit_restaurant_page(request):
    """Update restaurant data"""
    validate(instance=request.body, schema=restaurant_schema)
    body = json.loads(request.body)
    invalid = Restaurant.field_validate(body)
    if invalid is not None:
        return JsonResponse(invalid)
    restaurant = Restaurant.get(body["restaurant_id"])
    for field in body:
        if field in restaurant_editable:
            setattr(restaurant, field, body[field])
    if "address" in body:
        try:
            setattr(restaurant, 'GEO_location', geo_controller.geocode(body['address']))
        except ValueError:
            pass
    restaurant.clean_fields()
    restaurant.clean()
    restaurant.save()
    restaurant._id = str(restaurant._id)
    return JsonResponse(model_to_dict(restaurant))


def update_logo(request):
    """Upload file to cloud and set logo url to that file's url"""
    form = upload_form.ImageIdForm(request.POST, request.FILES)
    if form.is_valid():
        Restaurant.update_logo(request.FILES['image'], request.POST['_id'])
        return HttpResponse('SUCCESS')
    return HttpResponse('FAILURE')


def edit_dish_page(request):
    """Update Dish data"""
    validate(instance=request.body, schema=food_schema)
    body = json.loads(request.body)
    invalid = Food.field_validate(body)
    if invalid is not None:
        return JsonResponse(invalid)
    dish = Food.objects.get(_id=body["_id"])
    old_category = dish.category
    for field in body:
        if field in dish_editable:
            setattr(dish, field, body[field])
    dish.clean_fields()
    dish.clean()
    dish.save()
    if 'category' in body:
        category = body['category']  # New One
        restaurant = Restaurant.objects.get(_id=dish.restaurant_id)
        if category not in restaurant.categories:
            print('1')
            restaurant.categories.append(category)
            restaurant.save(update_fields=['categories'])
        if not Food.objects.filter(restaurant_id=restaurant._id, category=old_category).exists():
            restaurant.categories.remove(old_category)
            restaurant.save(update_fields=['categories'])
    return JsonResponse(model_to_json(dish))
