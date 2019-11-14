import itertools
import json

from google.cloud import storage

from app import config
from app import utils
from app.logger import logger


def get_latest_blobs_by_term():
    """Gets the latest blobs found in the processed bucket

    Returns a list of filenames that are the most recent file created
    for each term

    :return: A list blob representing the latest objects in the bucket
    """

    def term_code(blob_name):
        return blob_name.split("/")[0]

    storage_client = storage.Client()
    bucket_name = config.PROCESSED_BUCKET_NAME
    bucket = storage_client.lookup_bucket(bucket_name)

    if bucket is None:
        print("Bucket does not exist. Exiting program.")
        return None

    blobs = list(storage_client.list_blobs(bucket_name))
    blobs.sort(key=lambda x: x.name)
    logger.debug(f"blobs {blobs}")

    latest_blobs = [
        max(group, key=lambda x: x.name, default=None)
        for key, group in itertools.groupby(blobs, lambda x: term_code(x.name))
    ]

    return latest_blobs


def upload_to_bucket():
    """Uploads database to Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket_name = config.DATABASE_BUCKET_NAME
    bucket = storage_client.lookup_bucket(bucket_name)

    if bucket is None:
        bucket = storage_client.create_bucket(bucket_name)
        logger.debug("Bucket {} created.".format(bucket.name))
    else:
        logger.debug("Bucket {} already exists.".format(bucket.name))

    filename = utils.generate_filename()

    blob = bucket.blob(config.DATABASE_FILE)
    blob.upload_from_filename(config.DATABASE_FILE)
    bucket.rename_blob(blob, filename)

    logger.debug("File {} uploaded to {}.".format(filename, bucket_name))


def write_lambda_file(filename, contents):
    """Saves content to lambda filename.

    Saves contents to a filename and writes them to a /tmp/ directory in the Cloud Function.
    Cloud Functions only have write access to their /tmp/ directory.

    :param filename: The filename to write the data to.
    :param contents: The contents to put in the bucket.
    :return: The filename that the contents are written to.
    """
    lambda_filename = f"/tmp/{filename}"

    with open(lambda_filename, "w") as outfile:
        json.dump(contents, outfile)

    return lambda_filename
