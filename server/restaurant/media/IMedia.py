from cloud_storage import IMediaInterface
from restaurant.models import Food
from .form import FoodForm

class FoodMedia(IMediaInterface.IMedia):
    """Implement food for Imedia uploading"""

    def upload_and_save(self, post, files):
        """
        Implement uploading file to cloud and then saving in save location
        :return:
        """
        save_location = post['save_location']
        _id = post['_id']
        dish = Food.objects.get(_id=_id)  # search for object
        path = self.cloud.upload(files['file'], self.cloud.TEST_BUCKET,
                                 content_type=self.cloud.IMAGE)  # upload and save path
        setattr(dish, save_location, path)
        dish.save()
        return dish

    def validate(self, post, files):
        """Validate form"""
        form = FoodForm(post, files)
        print(form.errors)
        return form.is_valid()