from cloud_storage import cloud_controller
from abc import ABC, abstractmethod


class IMedia(ABC):
    """Interface for saving images in cloud bucket to appropriate database entry"""

    @abstractmethod
    def upload(self, post, files):
        """Configures parameters per endpoint for save method in IMedia"""
        pass

    def validate(self, post, files):
        form = self.form(post, files)
        return form.is_valid()

    def save(self, query, collection, path, save_location):
        """
        Generic code to save path new location in document identified by query
        :param query: query dictionary to isolate document
        :param collection: table collection
        :param path: path to new image
        :param save_location: save url
        :return: updated docuemnt
        """
        document = collection.objects.get(**query)  # search for object
        old_path = getattr(document, save_location)
        self.cloud.delete(old_path)
        setattr(document, save_location, path)
        document.save()
        return document

    def __init__(self):
        """Setup cloud controller for class"""
        self.cloud = cloud_controller
