import json
import os

from app import config
from app import storage
from app.database import dal
from app.database.manager import ClassOfferingMgr
from app.database.manager import CourseMgr
from app.database.manager import InstructorMgr
from app.database.manager import TermMgr
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


def write_to_database(contents):
    for term_code, term in contents.items():
        for course in term:
            save_to_database(course)


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
    cleanup_lambda_files()

    latest_blob = storage.get_latest_blob()
    contents = latest_blob.download_as_string()
    try:
        contents_json = json.loads(contents)
    except json.decoder.JSONDecodeError as e:
        logger.critical(f"Error decoding JSON: {e}")
        exit()

    dal.db_init()
    write_to_database(contents_json)

    return contents_json
