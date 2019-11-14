import json
import os

from app import config
from app import storage
from app.database import store
from app.logger import logger


def get_unique_instructors(instructor_list):
    """Transforms a list of instructors into a list of unique instructors

    :param instructor_list: List of instructors
    :return: Unique list of instructors
    """
    instructors = []
    for inst in instructor_list:
        instructors.append(inst)

    return filter_instructor_name(instructors)


def filter_instructor_name(instructors):
    """Filters instructors by name

    :param instructors: List of instructors
    :return: List of instructors with unique names
    """
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
        os.remove(config.DATABASE_FILE)
    except FileNotFoundError:
        pass


def run():
    """Runs the application

    :return: JSON representation of bucket contents
    """
    cleanup_lambda_files()

    latest_blobs = storage.get_latest_blobs_by_term()
    terms = [blob.download_as_string() for blob in latest_blobs]
    try:
        terms_json = [json.loads(term) for term in terms]
    except json.decoder.JSONDecodeError as e:
        logger.critical(f"Error decoding JSON: {e}")
        exit()

    store.write_to_database(terms_json)
    storage.upload_to_bucket()

    return terms_json
