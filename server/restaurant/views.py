from django.http import HttpResponse, JsonResponse
from restaurant.models import Food, ManualTag
from django.forms.models import model_to_dict
import json


def add_tag_page(request):
    body = json.loads(request.body)
    tag = ManualTag.add_tag(body['food_name'], body['restaurant_id'], body['category'], body['value'])
    return JsonResponse(model_to_dict(tag))


def clear_tags_page(request):
    body = json.loads(request.body)
    ManualTag.clear_food_tags(body['food_name'], body['restaurant'])
    return HttpResponse(status=200)


def get_food_by_restaurant_page(request):
    rest_id = request.GET.get('restaurant_id')

    return JsonResponse(Food.get_by_restaurant(rest_id))


def all_dishes_page(request):
    return JsonResponse(Food.get_all())


def create_dish_page(request):
    body = json.loads(request.body)
    food = Food.add_dish(body)
    food._id = str(food._id)
    return JsonResponse(model_to_dict(food))

def auto_tag(request):
    body = json.loads(request.body)
    tags = [model_to_dict(tag) for tag in ManualTag.auto_tag_food(body['_id'])]
    return JsonResponse({'tags' : tags})