from cloud_storage import IMediaInterface
from user.models import SDUser
from .form import SDUserForm


class SDUserMedia(IMediaInterface.IMedia):
    """Implement food for Imedia uploading"""

    def upload(self, post, files):
        """
        Implement uploading file to cloud and then saving in save location
        :return:
        """
        query = {'email': post['email']}
        path = self.cloud.upload(files['file'], self.cloud.TEST_BUCKET,
                                 content_type=self.cloud.IMAGE)  # upload and save path
        return self.save(query, SDUser, path, post['save_location'])

    def __init__(self):
        self.form = SDUserForm
        super().__init__()
