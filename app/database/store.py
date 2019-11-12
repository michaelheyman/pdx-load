from app.database import dal
from app.database.manager import ClassOfferingMgr
from app.database.manager import CourseMgr
from app.database.manager import InstructorMgr
from app.database.manager import TermMgr


def write_to_database(contents):
    dal.db_init()

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
