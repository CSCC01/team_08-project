from django.http import QueryDict


# Test case utilities

class TestHelper:

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


class MockModule:

    # save original and mock value
    def __init__(self, var, mock_obj):
        self.var = var
        self.mock_obj = mock_obj

    # replace original value with mock
    def mock(self):
        return self.mock_obj

    # replace mock value with mock
    def undo(self):
        return self.var

#used for mocking responses
class MockResponse:
    """
    params:
    
    """
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data