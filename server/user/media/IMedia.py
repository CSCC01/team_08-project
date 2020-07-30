from cloud_storage import IMediaInterface
from user.models import SDUser
from .form import SDUserForm


class SDUserMedia(IMediaInterface.IMedia):
    """Implement media upload for SDUser model"""

    def upload(self, post, files):
        """
        Configure parameters to save uploaded file to database
        :return: updated model
        """
        query = {'email': post['email']}
        path = self.cloud.upload(files['file'], self.cloud.TEST_BUCKET,
                                 content_type=self.cloud.IMAGE)  # upload and save path
        return self.save(query, SDUser, path, post['save_location'])

    def __init__(self):
        self.form = SDUserForm
        super().__init__()
