from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from restaurant.models import Food, ManualTag, Restaurant
from jsonschema import validate
import json
from utils.model_util import model_to_json, save_and_clean, edit_model, update_model_geo, models_to_json

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
    food_name, restaurant_id, category, value = \
        body['food_name'], body['restaurant_id'], body['category'], body['value']
    tag = ManualTag.add_tag(food_name, restaurant_id, category, value)
    return JsonResponse(model_to_json(tag))


def clear_tags_page(request):
    """Clear tags/food relationship"""
    validate(instance=request.body, schema=tag_schema)
    body = json.loads(request.body)
    ManualTag.clear_food_tags(body['food_name'], body['restaurant_id'])
    return HttpResponse(status=200)


def get_dish_by_restaurant_page(request):
    """Retrieve all dishes from a restaurant"""
    rest_id = request.GET.get('restaurant_id')
    dishes = Food.get_by_restaurant(rest_id)
    response = {'Dishes': models_to_json(dishes)}
    return JsonResponse(response)


def all_dishes_page(request):
    """Retrieve all dishes from the database"""
    foods = Food.objects.all()
    response = {'Dishes': models_to_json(foods)}
    return JsonResponse(response)


def insert_dish_page(request):
    """Insert dish into database"""
    validate(instance=request.body, schema=food_schema)
    body = json.loads(request.body)
    invalid = Food.field_validate(body)
    if invalid:
        return JsonResponse(invalid)
    food = Food.add_dish(body)
    return JsonResponse(model_to_json(food))


def delete_dish_page(request):
    """ Deletes dish from database """
    validate(instance=request.body, schema=tag_schema)
    body = json.loads(request.body)
    ManualTag.clear_food_tags(body["food_name"], body["restaurant_id"])
    food = Food.objects.get(name=body["food_name"], restaurant_id=body["restaurant_id"])
    food.delete()
    restaurant = Restaurant.objects.get(_id=body["restaurant_id"])
    if not category_exists(body["restaurant_id"], food.category):
        remove_category(food.category, restaurant)
    return HttpResponse(status=200)


def remove_category(category, restaurant):
    """
    remove category from restaurant
    @param category: food category
    @param restaurant: restaurant document
    """
    restaurant.categories.remove(category)
    restaurant.save(update_fields=['categories'])


def category_exists(restaurant_id, category):
    """
    check if restaurant still covers category 'category'
    @param restaurant:referenced restaurant
    @param category: category
    @return:boolean
    """
    return Food.objects.filter(restaurant_id=restaurant_id, category=category).exists()


def auto_tag_page(request):
    """Automatically generate tags for food"""
    validate(instance=request.body, schema=food_schema)
    body = json.loads(request.body)
    tags = models_to_json(ManualTag.auto_tag_food(body['_id']))
    return JsonResponse({'tags': tags})


def get_restaurant_page(request):
    """retrieve restaurant by id"""
    _id = request.GET.get('_id')

    restaurant = Restaurant.get(_id)
    if restaurant:
        return JsonResponse(model_to_json(restaurant))
    else:
        return JsonResponse({})


def get_all_restaurants_page(request):
    """Retrieve all restaurants"""
    restaurants = list(Restaurant.objects.all())
    response = {'Restaurants': models_to_json(restaurants)}
    return JsonResponse(response)


def insert_restaurant_page(request):
    """Insert new restaurant into database"""
    validate(instance=request.body, schema=restaurant_schema)
    body = json.loads(request.body)
    invalid = Restaurant.field_validate(body)
    if invalid:
        return JsonResponse(invalid)
    try:
        restaurant = Restaurant.insert(body)
        return JsonResponse(model_to_json(restaurant))
    except ValueError:
        return HttpResponseBadRequest('duplicate email')


def edit_restaurant_page(request):
    """Update restaurant data"""
    validate(instance=request.body, schema=restaurant_schema)
    body = json.loads(request.body)
    invalid = Restaurant.field_validate(body)
    if invalid:  # exit if invalid body
        return JsonResponse(invalid)
    restaurant = Restaurant.get(body["restaurant_id"])
    edit_model(restaurant, body, restaurant_editable)
    if address_changed(body):
        update_model_geo(restaurant, body['address'])
    restaurant = save_and_clean(restaurant)
    return JsonResponse(model_to_json(restaurant))


def address_changed(body):
    """
    return if address has changed
    @param body: edited fields
    @return: boolean
    """
    return 'address' in body


def edit_dish_page(request):
    """Update Dish data"""
    # validation
    validate(instance=request.body, schema=food_schema)
    body = json.loads(request.body)
    invalid = Food.field_validate(body)
    if invalid is not None:
        return JsonResponse(invalid)

    dish = Food.objects.get(_id=body["_id"])
    restaurant = Restaurant.objects.get(_id=dish.restaurant_id)
    if should_add_category(body, dish.category, restaurant):    # add category if new
        add_cateogory(dish.category, restaurant)

    # edit model
    edit_model(dish, body, dish_editable)
    dish = save_and_clean(dish)

    # if category has been edited, may remove old category
    if category_is_changed(body) and category_exists(body['category'], restaurant._id):
        remove_category(body['category', restaurant])
    return JsonResponse(model_to_json(dish))


def category_is_changed(body):
    """
    check whether category was edited
    @param body: request body for editing
    @return: boolean
    """
    return 'category' in body


def new_category(category, restaurant):
    """
    check if category is new to restaurant
    @param category: restaurant category
    @param restaurant: referenced restaurant
    @return: boolean
    """
    return category in restaurant.categories


def should_add_category(body, category, restaurant):
    """
    check if should add category
    @param body:
    @param category:
    @param restaurant:
    @return:
    """
    return category_is_changed(body) and new_category(category, restaurant)


def add_cateogory(category, restaurant):
    """
    add new category to restaurant
    @param category:
    @param restaurant:
    @return:
    """
    restaurant.categories.append(category)
    restaurant.save(update_fields=['categories'])
