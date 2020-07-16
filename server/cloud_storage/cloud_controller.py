# Module to upload files to the cloud
from google.cloud import storage

client = storage.Client.from_service_account_json('scdining.json')
TEST_BUCKET = 'test-storage-nog'
PRODUCTION_BUCKET = ''
BUCKET=TEST_BUCKET


def upload_blob():
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    bucket = client.bucket(BUCKET)
    name = 'test1'
    blob = bucket.blob(name)
    blob.upload_from_filename("C:\\Users\\Alac Wang\\Downloads\\flat,750x1000,075,f.jpg")

    return 'https://storage.googleapis.com/' + BUCKET + name



if __name__ == '__main__':
    upload_blob()
