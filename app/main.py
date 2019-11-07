import json

from google.cloud import firestore
from google.cloud import storage

from app import config
from app.logger import logger
# from app.firestore import Firestore

example_data = [
    [
        {
            "number": "ACTG 281",
            "name": "ACCOUNTING MECHANICS: DR & CR",
            "crn": 10002,
            "discipline": "Accounting",
            "days": "",
            "credits": 1,
            "time": None,
            "instructor": {
                "fullName": "Marilyn L Johnson",
                "firstName": "Marilyn",
                "lastName": "Johnson",
                "rating": 2.88,
                "rmpId": 497_275,
            },
            "term_description": "Fall 2019",
            "term_date": 201_904,
        },
        {
            "number": "ACTG 281",
            "name": "ACCOUNTING MECHANICS: DR & CR",
            "crn": 14758,
            "discipline": "Accounting",
            "days": "F",
            "credits": 1,
            "time": "13:30 - 15:00",
            "instructor": {
                "fullName": "Marilyn L Johnson",
                "firstName": "Marilyn",
                "lastName": "Johnson",
                "rating": 2.88,
                "rmpId": 497_275,
            },
            "term_description": "Fall 2019",
            "term_date": 201_904,
        },
    ]
]


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


def get_firestore_instructors():
    # issue a request to get the list of instructors
    pass


def get_unique_instructors(data):
    instructors = set()
    lst = list()
    for term in data:
        for course in term:
            instructors.add(course["instructor"])  # ERROR: can't add dicts to set
            # how do we get unique values, or remove duplicates from a list w/o sets?


def add_firestore_instructors(client, instructors):
    # adds instructors to firestore if they don't exist yet
    #
    instructor_ref = client.collection("instructors")

    # get all instructor information locally and store it in some globally accessible variable
    firestore_instructors = get_firestore_instructors(client)
    # check for instructors that have to be updated and added
    # add them to the local structure
    # push the structure back to the datastore in a batch


def get_firestore_instructors(client):
    instructor_ref = client.collection("instructors")

    return [instructor.to_dict() for instructor in instructor_ref]


def add_firestore_courses(client, courses):
    # get all the instructor information locally (maybe from the `add_firestore_instructors call`)
    # associate the instructor in the course information with the unique datastore identifier
    # create the structure expected for a datastore course entity
    # push it with the instructor object reference in a batch
    pass


def initialize_firestore():
    # nuke all the contents of the datastore -- for now
    # TODO: nuke only the contents of the terms that are being added to the database, w/o nuking instructors
    client = firestore.Client()
    pass


def parse_terms_into_instructors(contents):
    instructors = [x["instructor"] for x in contents]
    return instructors


def run():
    with open("processed-data.json") as json_file:
        import json

        contents = json.loads(json_file.read())
    # parse_terms_into_instructors(contents[0])
    # latest_blob = get_latest_blob()
    # contents = latest_blob.download_as_string()
    # try:
    #     contents_json = json.loads(contents)
    # except json.decoder.JSONDecodeError as e:
    #     logger.critical(f"Error decoding JSON: {e}")
    #     exit()
    # return contents_json

    initialize_firestore()

    print("done")
    return example_data
