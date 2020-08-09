from .encoder import BSONEncoder
from django.forms import model_to_dict
import json
from geo import geo_controller


def save_and_clean(model, updated_fields=None):
    """
    clean model and then save
    :params-model: referenced model
    :return: saved model
    """
    model.clean_fields()
    model.clean()
    if updated_fields:
        model.save(updated_fields)
    else:
        model.save()
    return model


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


def edit_model(model, body, editable):
    """
    Edit model data
    @param model: model to be edited
    @param body: body of fields
    @param editable: list of editable fields
    @return:
    """
    editable_fields = list(set(body) & set(editable))
    for editable_field in editable_fields:
        setattr(model, editable_field, body[editable_field])


def update_model_geo(model, address):
    try:
        model.GEO_location = geo_controller.geocode(address)
    except ValueError:
        pass
    return model
