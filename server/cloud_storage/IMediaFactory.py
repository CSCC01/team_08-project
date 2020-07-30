from .AppType import AppCollection
from importlib import import_module

factory = {}

for app in AppCollection:  # import all imedia implementations and store in dictionary
    [app_name, collection_name] = app.name.split('_')
    module = app_name + '.media.IMedia'
    # Retrieve class after loading module
    factory[app.name] = getattr(import_module(module), collection_name)()
