from .AppType import AppCollection
from importlib import import_module

IMedia_dict = {}

for app in AppCollection:    # import all imedia implementations and store in dictionary
    [app_name, collection_name] = app.value.split('/')
    module = app_name + '.media.IMedia'
    IMedia_dict[app.value] = getattr(import_module(module), collection_name)()