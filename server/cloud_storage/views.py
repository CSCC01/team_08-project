from django.http import JsonResponse, HttpResponseBadRequest
from .form import MediaForm
from utils.encoder import BSONEncoder
import json
from .IMediaFactory import factory
from django.forms import model_to_dict


def media_upload_page(request):
    """
    :param request: Multi-part form request
    :return: document with updated link
    """
    form = MediaForm(request.POST, request.FILES)  # Initial validation
    if form.is_valid():  # initial validate form
        IMedia = factory[request.POST['app']]
        if IMedia.validate(request.POST, request.FILES):    # App Validation
            model = model_to_dict(IMedia.upload_and_save(request.POST, request.FILES))
            return JsonResponse(json.loads(json.dumps(model, cls=BSONEncoder)))
        else:
            return HttpResponseBadRequest('Invalid form')
    return HttpResponseBadRequest('Invalid form')
