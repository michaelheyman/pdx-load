import json
import os

from google.cloud import storage

from app import config
from app.database import initialize_database
from app.logger import logger
from app.manager import ClassOfferingMgr
from app.manager import CourseMgr
from app.manager import InstructorMgr
from app.manager import TermMgr


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


def load_local_file():
    local_file = "snapshot.json"
    local_filename = os.path.join(config.PROJECT_DIR, local_file)
    res = None
    with open(local_filename) as infile:
        res = json.load(infile)

    return res


def get_unique_instructors(instructor_list):
    instructors = []
    for inst in instructor_list:
        instructors.append(inst)

    return filter_instructor_name(instructors)


def filter_instructor_name(instructors):
    return list({v["fullName"]: v for v in instructors}.values())


def extract_metadata(contents):
    """Extracts course and instructor information from the bucket metadata

    :param contents: Bucket metadata
    :return: list of terms, courses, and instructors
    """

    terms = []
    instructors = []
    courses = []
    for term in contents:
        for course in term:
            courses.append(course)
            instructors.append(course["instructor"])

    return terms, courses, instructors


def write_to_database(contents):
    terms, courses, instructors = extract_metadata(contents)


def save_to_database(course):
    if course["instructor"] is None:  # NOTE: are there ever NO instructors?
        CourseMgr.add_course(
            name=course["name"],
            number=course["number"],
            discipline=course["discipline"],
        )
        return

    InstructorMgr.add_instructor(course["instructor"])
    CourseMgr.add_course(
        name=course["name"], number=course["number"], discipline=course["discipline"]
    )

    ClassOfferingMgr.add_class_offering(
        course_name=course["name"],
        course_number=course["number"],
        # instructor_name=course["instructor"],
        # TODO: how can we get a default value for this access,
        #  like course.get(["instructor"]["fullName"], None)?
        instructor_name=course["instructor"]["fullName"]
        if course["instructor"]
        else None,
        term=course["term_date"],
        credits=course["credits"],
        days=course["days"],
        time=course["time"],
        crn=course["crn"],
    )

    TermMgr.add_term(date=course["term_date"], description=course["term_description"])


def cleanup_lambda_files():
    # this won't be necessary in the lambda because it won't save state
    try:
        os.remove(config.DATABASE_PATH)
    except FileNotFoundError:
        pass


def run():
    contents = load_local_file()  # TODO: remove after testing
    cleanup_lambda_files()
    initialize_database()
    for term in contents:
        for course in term:
            save_to_database(course)
    # write_to_database(contents)

    # latest_blob = get_latest_blob()
    # contents = latest_blob.download_as_string()
    # try:
    #     contents_json = json.loads(contents)
    # except json.decoder.JSONDecodeError as e:
    #     logger.critical(f"Error decoding JSON: {e}")
    #     exit()
    # return contents_json
