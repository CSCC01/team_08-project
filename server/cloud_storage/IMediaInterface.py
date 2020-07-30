from . import cloud_controller
from abc import ABC, abstractmethod


class IMedia(ABC):
    """Interface for saving images in cloud bucket to appropriate database entry"""

    @abstractmethod
    def upload_and_save(self, post, files):
        """Configures parameters per endpoint for save method in IMedia"""
        pass

    def validate(self, post, files):
        form = self.form(post, files)
        return form.is_valid()

    def upload(self, file, content_type, bucket=None):
        """Upload media to cloud"""
        if bucket is None:  # default bucket is set, allow option to change bucket
            bucket = self.bucket
        return self.cloud.upload(file, bucket, content_type)

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
        """Setup cloud controller constants"""
        self.cloud = cloud_controller
        self.bucket = cloud_controller.TEST_BUCKET
