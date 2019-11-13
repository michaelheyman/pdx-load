from datetime import datetime

from app.database import dal
from app.database.entities import ClassOffering
from app.database.entities import Course
from app.database.entities import Instructor
from app.database.entities import Term
from app.logger import logger


class ClassOfferingMgr:
    @staticmethod
    def add_class_offering(
        course_name, course_number, instructor_name, term, credits, days, time, crn
    ):
        """Adds a ClassOffering to the database

        :param course_name: Name of the course
        :param course_number: Number of the course
        :param instructor_name: Name of the instructor
        :param term: Term code
        :param credits: Number of credits
        :param days: Days the class is offered
        :param time: Time the class is offered at
        :param crn: CRN of the class
        :return: Database record of the inserted ClassOffering
        """
        course_id = (
            dal.DBSession.query(Course.course_id)
            .filter(Course.name == course_name, Course.number == course_number)
            .scalar()
        )
        instructor_id = (
            dal.DBSession.query(Instructor.instructor_id)
            .filter(Instructor.full_name == instructor_name)
            .scalar()
        )

        class_offering_record = (
            dal.DBSession.query(ClassOffering)
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

            dal.DBSession.add(class_offering_record)
            dal.DBSession.flush()
        else:
            class_offering_record.timestamp = datetime.now()

        dal.DBSession.commit()

        return class_offering_record


class CourseMgr:
    @staticmethod
    def add_course(name, number, discipline):
        """Adds a Course to the database.

        :param name: Name of the course
        :param number: Number of the course
        :param discipline: Discipline of the course
        :return: None
        """
        exists = (
            dal.DBSession.query(Course)
            .filter(
                Course.name == name,
                Course.number == number,
                Course.discipline == discipline,
            )
            .first()
        ) is not None

        if not exists:
            course = Course(name=name, number=number, discipline=discipline)
            dal.DBSession.add(course)
            dal.DBSession.commit()


class InstructorMgr:
    @staticmethod
    def add_instructor(instructor):
        """Adds an Instructor to the database.

        :param instructor: Instructor dictionary
        :return: Database record of the inserted Instructor
        """
        instructor_record = (
            dal.DBSession.query(Instructor)
            .filter(Instructor.full_name == instructor["fullName"])
            .first()
        )

        if instructor_record is None:
            logger.debug("Creating new instructor.", extra={"instructor": instructor})
            instructor_record = InstructorMgr.create_instructor(instructor)

            dal.DBSession.add(instructor_record)

        dal.DBSession.commit()

        return instructor_record

    @staticmethod
    def create_instructor(instructor):
        """Creates an instructor

        :param instructor: Instructor dictionary
        :return: Instructor ORM representation
        """
        if all("fullName" in key for key in instructor.keys()):
            logger.info(
                "No metadata for this instructor",
                extra={"instructor": instructor["fullName"]},
            )
            return Instructor(full_name=instructor["fullName"])

        return Instructor(
            full_name=instructor["fullName"],
            first_name=instructor["firstName"],
            last_name=instructor["lastName"],
            rating=instructor["rating"],
            url=f"http://www.ratemyprofessors.com/ShowRatings.jsp?tid={instructor['rmpId']}",
        )


class TermMgr:
    @staticmethod
    def add_term(date, description):
        """Adds a Term to the database

        :param date: Date of the term
        :param description: Descriptoin of the term
        :return: Database record of the inserted Term
        """
        term_record = (
            dal.DBSession.query(Term)
            .filter(Term.date == date, Term.description == description)
            .first()
        )

        if term_record is None:
            term_record = Term(date=date, description=description)

            dal.DBSession.add(term_record)
            dal.DBSession.flush()
            dal.DBSession.commit()

        return term_record
