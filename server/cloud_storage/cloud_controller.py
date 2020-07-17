# Module to upload files to the cloud
from google.cloud import storage
import datetime
import string
import random

client = storage.Client.from_service_account_json('scdining.json')
TEST_BUCKET = 'test-storage-nog'
PRODUCTION_BUCKET = 'production-scdining'


def upload(file, bucket_path):
    """Uploads a file to the bucket."""
    bucket = client.bucket(bucket_path)
    name = generate_name()
    blob = bucket.blob(name)
    blob.upload_from_file(file)
    return 'https://storage.googleapis.com/' + bucket_path + '/' + name


def generate_name():
    name = str(datetime.datetime.now())
    letters = string.ascii_lowercase
    name += (''.join(random.choice(letters) for i in range(10)))
    name += '.png'
    return name


def delete_object():
    """TODO implements this when you get list of defaults"""
