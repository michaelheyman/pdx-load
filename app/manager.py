from datetime import datetime

from app.database.model import ClassOffering
from app.database.model import Course
from app.database.model import DBSession
from app.database.model import Instructor
from app.database.model import Term
from app.logger import logger


class ClassOfferingMgr:
    @staticmethod
    def add_class_offering(
        course_name, course_number, instructor_name, term, credits, days, time, crn
    ):
        course_id = (
            DBSession.query(Course.course_id)
            .filter(Course.name == course_name, Course.number == course_number)
            .scalar()
        )
        instructor_id = (
            DBSession.query(Instructor.instructor_id)
            .filter(Instructor.full_name == instructor_name)
            .scalar()
        )

        class_offering_record = (
            DBSession.query(ClassOffering)
            .filter(
                ClassOffering.term == term,
                ClassOffering.course_id == course_id,
                ClassOffering.instructor_id == instructor_id,
                ClassOffering.crn == crn,
                ClassOffering.credits == credits,
            )
            .first()
        )

        if class_offering_record is None:
            class_offering_record = ClassOffering(
                course_id=course_id,
                instructor_id=instructor_id,
                term=term,
                credits=credits,
                crn=crn,
                days=days,
                time=time,
            )

            DBSession.add(class_offering_record)
            DBSession.flush()
        else:
            class_offering_record.timestamp = datetime.now()

        DBSession.commit()

        return class_offering_record


class CourseMgr:
    @staticmethod
    def add_course(name, number, discipline):
        exists = (
            DBSession.query(Course)
            .filter(
                Course.name == name,
                Course.number == number,
                Course.discipline == discipline,
            )
            .first()
        ) is not None

        if not exists:
            course = Course(name=name, number=number, discipline=discipline)
            DBSession.add(course)
            DBSession.commit()


class InstructorMgr:
    @staticmethod
    def add_instructor(instructor):
        instructor_record = (
            DBSession.query(Instructor)
            .filter(Instructor.full_name == instructor["fullName"])
            .first()
        )

        if instructor_record is None:
            logger.debug("Creating new instructor.", extra={"instructor": instructor})
            instructor_record = InstructorMgr.create_instructor(instructor)

            DBSession.add(instructor_record)
            # DBSession.flush()

        DBSession.commit()

        return instructor_record

    @staticmethod
    def create_instructor(instructor):
        if all("fullName" in key for key in instructor.keys()):
            logger.info(
                "No metadata for this instructor",
                extra={"instructor": instructor["fullName"]},
            )
            return Instructor(full_name=instructor["fullName"])

        return Instructor(
            full_name=instructor["fullName"],
            first_name=instructor["firstName"],
            last_name=instructor["firstName"],
            rating=instructor["rating"],
            url=f"http://www.ratemyprofessors.com/ShowRatings.jsp?tid={instructor['rmpId']}",
        )


class TermMgr:
    @staticmethod
    def add_term(date, description):
        term_record = (
            DBSession.query(Term)
            .filter(Term.date == date, Term.description == description)
            .first()
        )

        if term_record is None:
            term_record = Term(date=date, description=description)

            DBSession.add(term_record)
            DBSession.flush()
            DBSession.commit()

        return term_record
