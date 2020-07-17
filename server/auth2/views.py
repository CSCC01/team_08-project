from django.http import HttpResponse, JsonResponse
from auth2.models import SDUser
from RO.models import Restaurant
import json


def signup_page(request):
    body = json.loads(request.body)
    user = SDUser.signup(nickname=body['nickname'], name=body['name'], picture=body['picture'],
                         updated=body['updated_at'], email=body['email'],
                         verified=body['email_verified'], role=body['role'], restaurant_id=body['restaurant_id'])
    return HttpResponse(status=200)


def reassign_page(request):
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
    req_email = request.GET.get('email')
    user = SDUser.objects.get(pk=req_email)
    return JsonResponse(
        {'nickname': user.nickname, 'name': user.name, 'picture': user.picture, 'updated_at': user.last_updated,
         'email': user.email, 'email_verified': user.email_verified, 'role': user.role})


def exists_page(request):
    req_email = request.GET.get('email')
    return JsonResponse({'exists': SDUser.objects.filter(email=req_email).exists()})
