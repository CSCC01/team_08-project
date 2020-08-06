class Mock_Controller: # Class for mocking behaviour found in cloud_controller
    TEST_BUCKET = 'test'
    PRODUCTION_BUCKET = 'test'
    IMAGE= 'test'
    def upload(self, file, bucket_path, content_type=None):
        return "test_path"

    def delete(self, file_path):
        return('delete')

