from .encoder import BSONEncoder
from django.forms import model_to_dict
import json


def model_to_json(model, extra_params={}):
    """
    utility function for handling converting models to json serializable dicts
    :params-model: model you are converting
    :params-extra_params: extra parameters you want to include in the returned dict
    :return: dictionary containing all fields in the model converted to json serializable form
    """

    model_dict = model_to_dict(model)
    for elem in extra_params:
        model_dict[elem] = extra_params[elem]

    return json.loads(json.dumps(model_dict, cls=BSONEncoder))
