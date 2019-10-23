import json

from google.cloud import storage

from app import config
from app.logger import logger


def get_latest_blob():
    """ Gets the latest blob found in the unprocessed bucket

    Return:
        Blob: A blob representing the object in the bucket
    """
    storage_client = storage.Client()
    bucket_name = config.PROCESSED_BUCKET_NAME
    bucket = storage_client.lookup_bucket(bucket_name)

    if bucket is None:
        print("Bucket does not exist. Exiting program.")
        return None

    blobs = list(storage_client.list_blobs(bucket_name))
    logger.debug(f"blobs {blobs}")
    latest_blob = max(blobs, key=lambda x: x.name, default=None)

    return latest_blob


def run():
    latest_blob = get_latest_blob()
    contents = latest_blob.download_as_string()
    try:
        contents_json = json.loads(contents)
    except json.decoder.JSONDecodeError as e:
        logger.critical(f"Error decoding JSON: {e}")
        exit()
    return contents_json
