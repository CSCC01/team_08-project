from cloud_storage import IMediaInterface
from user.models import SDUser
from .form import SDUserForm


class SDUserMedia(IMediaInterface.IMedia):
    """Implement media upload for SDUser model"""

    def upload_and_save(self, post, files):
        """
        Configure parameters to save uploaded file to database
        :return: updated model
        """
        query = {'email': post['email']}
        # not defining image constant bc media content_type changes (could be video)
        path = self.upload(files['file'], self.cloud.IMAGE)  # upload and save path
        return self.save(query, SDUser, path, post['save_location'])

    def __init__(self):
        self.form = SDUserForm
        super().__init__()
