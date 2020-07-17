from django.http import JsonResponse
import json
from RO.models import Restaurant
from django.forms.models import model_to_dict
from django.http import HttpResponse
from request_form import upload_form


# Create your views here.
def get(request):
    try:  # body
        body = json.loads(request.body)
        _id = body['_id']
    except:  # query string
        _id = request.GET.get('_id')

    restaurant = Restaurant.get(_id)
    if restaurant:
        return JsonResponse(model_to_dict(restaurant))
    else:
        return JsonResponse({})


def get_all(request):
    return JsonResponse(Restaurant.get_all())


def insert(request):
    restaurant = Restaurant.insert(json.loads(request.body))
    restaurant._id = str(restaurant._id)
    return JsonResponse(model_to_dict(restaurant))


def update_logo(request):
    form = upload_form.ImageIdForm(request.POST, request.FILES)
    url = 'FAILED'
    if form.is_valid():
        url = Restaurant.update_logo(request.FILES['image'], request.POST['_id'])
    return JsonResponse({'url' : url})