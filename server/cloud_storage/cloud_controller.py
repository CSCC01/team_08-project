# Module to upload files to the cloud
from google.cloud import storage
import datetime
import string
import random

client = storage.Client.from_service_account_json('scdining.json')
TEST_BUCKET = 'test-storage-nog'
PRODUCTION_BUCKET = 'production-scdining'
API = 'https://storage.googleapis.com/'


def upload(file, bucket_path, content_type=None):
    """Uploads a file to the bucket path."""
    bucket = client.bucket(bucket_path)
    name = generate_name()
    blob = bucket.blob(name)
    blob.upload_from_file(file, content_type=content_type)
    return API + bucket_path + '/' + name


def generate_name():
    """Generate a randomized filename"""
    letters = string.ascii_lowercase
    name = 'FILE-' + (''.join(random.choice(letters) for i in range(10))) + '-' + \
           str(datetime.datetime.now()) + '.png'
    return name


def delete(file_path):
    """
    delete object from bucket if it is not a default
    """

    if 'default-assets' in file_path:
        return
    elif API == file_path[:len(API)]:
        file_path.replace(API, '')
        bucket_path = file_path[:file_path.find('/')]
        bucket = client.bucket(bucket_path)
        bucket.delete_blob(file_path[file_path.find('/') + 1:])
    else:
        print('cannot parse invalid file')
