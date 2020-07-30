import json
from django.forms import model_to_dict
from django.http import QueryDict
from .encoder import BSONEncoder

# Test case utilities

class TestHelper:
    def process_expected(self, model):
        """Reloads model from db, and trasnforms it into a dictionary"""
        model.refresh_from_db()
        return json.loads(json.dumps(model_to_dict(model), cls=BSONEncoder))

    # Not an elegant solution, however due to the bug in django
    # where multipart form request should produce a mutable POST field but doesn't
    # I have to use this fix, however if you can find me a better fix, I can implement it
    def process_request(self, request, post, files):
        """Populate request with multi-part data"""
        request.FILES.update(files)
        request.POST = QueryDict('', mutable=True)
        request.POST.update(post)
        request.POST._mutable = False
        return request
