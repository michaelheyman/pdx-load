import json
import os

from app import config
from app import storage
from app.database import store
from app.logger import logger


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


def cleanup_lambda_files():
    # this won't be necessary in the lambda because it won't save state
    try:
        os.remove(config.DATABASE_PATH)
    except FileNotFoundError:
        pass


def run():
    cleanup_lambda_files()

    latest_blob = storage.get_latest_blob()
    contents = latest_blob.download_as_string()
    try:
        contents_json = json.loads(contents)
    except json.decoder.JSONDecodeError as e:
        logger.critical(f"Error decoding JSON: {e}")
        exit()

    store.write_to_database(contents_json)
    storage.upload_to_bucket()

    return contents_json
