from django.http import HttpResponse, JsonResponse
from restaurant.models import Food, ManualTag, Restaurant
from django.forms.models import model_to_dict
from jsonschema import validate
import json

# jsonschema validation schemes
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
        "exernal_delivery_link": {"type": "string"},
        "cover_photo_url": {"type": "string"},
        "logo_url": {"type": "string"},
        "rating": {"type": "string"},
    }
}


def insert_tag_page(request):
    """Insert tag to database"""
    validate(instance=request.body, schema=tag_schema)
    body = json.loads(request.body)
    tag = ManualTag.add_tag(body['food_name'], body['restaurant_id'], body['category'], body['value'])
    return JsonResponse(model_to_dict(tag))


def clear_tags_page(request):
    """Clear tags/food relationship"""
    # validate(instance=request.body, schema=tag_schema)
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
    food = Food.add_dish(body)
    food._id = str(food._id)
    return JsonResponse(model_to_dict(food))


def delete_dish_page(request):
    """Insert dish into database"""
    validate(instance=request.body, schema=tag_schema)
    body = json.loads(request.body)
    ManualTag.clear_food_tags(body["food_name"], body["restaurant_id"])
    Food.objects.filter(name=body["food_name"], restaurant_id=body["restaurant_id"]).delete()
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
    restaurant = Restaurant.insert(json.loads(request.body))
    restaurant._id = str(restaurant._id)
    return JsonResponse(model_to_dict(restaurant))


def edit_restaurant_page(request):
    """Update restaurant data"""
    validate(instance=request.body, schema=restaurant_schema)
    body = json.loads(request.body)
    restaurant = Restaurant.get(body["restaurant_id"])
    del body['restaurant_id']
    for field in body:
        if body[field] != "":
            setattr(restaurant, field, body[field])
    restaurant.clean_fields()
    restaurant.clean()
    restaurant.save()
    return HttpResponse(status=200)


def edit_dish_page(request):
    """Update Dish data"""
    validate(instance=request.body, schema=food_schema)
    body = json.loads(request.body)
    dish = Food.objects.get(_id=body["_id"])
    del body['_id']
    for field in body:
        setattr(dish, field, body[field])
    dish.clean_fields()
    dish.clean()
    dish.save()
    return HttpResponse(status=200)
