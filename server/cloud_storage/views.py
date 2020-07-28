from django.http import HttpResponse
from .request_form import MediaForm
from .AppType import Apps_Collection
from importlib import import_module

def media_upload_page(request):
    """
    :param request: Multi-part form request
    :return: document with updated link
    """
    form = MediaForm(request.POST, request.FILES) # initial validation
    x = import_module('restaurant.models')
    for app in Apps:
        print(app.value, type(app.value))
    print(request.POST['test'], type(request.POST['test']))
    if form.is_valid(): # validate form
        return HttpResponse('success')

    return HttpResponse('failure')


