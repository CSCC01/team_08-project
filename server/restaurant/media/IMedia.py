from cloud_storage import IMediaInterface
from restaurant.models import Food, Restaurant
from .form import FoodForm, RestaurantForm


class FoodMedia(IMediaInterface.IMedia):
    """Implement media upload for Food model"""

    def upload(self, post, files):
        """
        Configure parameters to save uploaded file to database
        :return: updated model
        """
        query = {'_id': post['_id']}
        path = self.cloud.upload(files['file'], self.cloud.TEST_BUCKET,
                                 content_type=self.cloud.IMAGE)  # upload and save path
        return self.save(query, Food, path, post['save_location'])

    def __init__(self):
        self.form = FoodForm
        super().__init__()


class RestaurantMedia(IMediaInterface.IMedia):
    """Implement media upload for restaurant model"""

    def upload(self, post, files):
        """
        Configure parameters to save uploaded file to database
        :return: updated model
        """
        query = {'_id': post['_id']}
        path = self.cloud.upload(files['file'], self.cloud.TEST_BUCKET,
                                 content_type=self.cloud.IMAGE)  # upload and save path
        return self.save(query, Restaurant, path, post['save_location'])

    def __init__(self):
        self.form = RestaurantForm
        super().__init__()

