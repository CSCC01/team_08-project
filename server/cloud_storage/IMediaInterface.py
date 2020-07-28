from cloud_storage import cloud_controller
from abc import ABC, abstractmethod


class IMedia(ABC):
    """
    Interface for saving images in cloud bucket to appropriate database entry
    """

    @abstractmethod
    def upload_and_save(self, form):
        pass

    def __init__(self):
        self.uploader = cloud_controller
