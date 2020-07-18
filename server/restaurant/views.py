from django.http import HttpResponse, JsonResponse
from restaurant.models import Food, ManualTag, Restaurant
from django.forms.models import model_to_dict
import json


def insert_tag_page(request):
    body = json.loads(request.body)
    tag = ManualTag.add_tag(body['food_name'], body['restaurant_id'], body['category'], body['value'])
    return JsonResponse(model_to_dict(tag))


def clear_tags_page(request):
    body = json.loads(request.body)
    ManualTag.clear_food_tags(body['food_name'], body['restaurant'])
    return HttpResponse(status=200)


def get_dish_by_restaurant_page(request):
    rest_id = request.GET.get('restaurant_id')
    return JsonResponse(Food.get_by_restaurant(rest_id))


def all_dishes_page(request):
    return JsonResponse(Food.get_all())


def insert_dish_page(request):
    body = json.loads(request.body)
    food = Food.add_dish(body)
    food._id = str(food._id)
    return JsonResponse(model_to_dict(food))


def auto_tag_page(request):
    
    body = json.loads(request.body)
    tags = [model_to_dict(tag) for tag in ManualTag.auto_tag_food(body['_id'])]
    print(tags)
    return JsonResponse({'tags': tags})


def get_restaurant_page(request):

    _id = request.GET.get('_id')

    restaurant = Restaurant.get(_id)
    if restaurant:
        return JsonResponse(model_to_dict(restaurant))
    else:
        return JsonResponse({})


def get_all_restaurants_page(request):
    return JsonResponse(Restaurant.get_all())


def insert_restaurant_page(request):
    restaurant = Restaurant.insert(json.loads(request.body))
    restaurant._id = str(restaurant._id)
    return JsonResponse(model_to_dict(restaurant))


def edit_restaurant_page(request):
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
