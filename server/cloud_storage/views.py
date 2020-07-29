from django.http import JsonResponse, HttpResponseBadRequest
from .form import MediaForm
from utils.encoder import BSONEncoder
import json
from .IMedia import IMedia_dict
from django.forms import model_to_dict


def media_upload_page(request):
    """
    :param request: Multi-part form request
    :return: document with updated link
    """
    form = MediaForm(request.POST, request.FILES)  # initial validation
    if form.is_valid():  # validate form
        imedia = IMedia_dict[request.POST['app']]
        if imedia.validate(request.POST, request.FILES):
            model = model_to_dict(imedia.upload(request.POST, request.FILES))
            return JsonResponse(json.loads(json.dumps(model, cls=BSONEncoder)))
        else:
            return HttpResponseBadRequest('Invalid form')
    return HttpResponseBadRequest('Invalid form')
