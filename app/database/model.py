from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database import Base


class ClassOffering(Base):
    __tablename__ = "ClassOffering"

    class_offering_id = Column("ClassOfferingId", Integer, primary_key=True)
    course_id = Column(
        "CourseId", Integer, ForeignKey("Course.CourseId"), nullable=False
    )
    course = relationship("Course")
    instructor_id = Column(
        "InstructorId", Integer, ForeignKey("Instructor.InstructorId")
    )
    instructor = relationship("Instructor")
    term = Column("Term", Integer, ForeignKey("Term.Description"))
    credits = Column("Credits", Integer, nullable=False)
    days = Column("Days", String)
    time = Column("Time", String)
    crn = Column("CRN", Integer, nullable=False)
    timestamp = Column("Timestamp", DateTime, default=datetime.now)

    def __repr__(self):
        return (
            f"<ClassOfferingId(id={self.class_offering_id}, "
            f"course_id={self.course_id}, "
            f"instructor_id={self.instructor_id}, "
            f"credits={self.credits}, "
            f"days={self.days}, "
            f"time={self.time}, "
            f"crn={self.crn}, "
            f"timestamp={self.timestamp})>"
        )


class Course(Base):
    __tablename__ = "Course"

    course_id = Column("CourseId", Integer, primary_key=True)
    name = Column("Name", String, nullable=False)
    number = Column("Class", String, nullable=False)
    discipline = Column("Discipline", String, nullable=False)

    def __repr__(self):
        return (
            f"<Course(id={self.course_id}, "
            f"name={self.name}, "
            f"number={self.number}, "
            f"discipline={self.discipline}, "
        )


class Instructor(Base):
    __tablename__ = "Instructor"

    instructor_id = Column("InstructorId", Integer, primary_key=True)
    full_name = Column("FullName", String, nullable=False)
    first_name = Column("FirstName", String)
    last_name = Column("LastName", String)
    rating = Column("Rating", Float)
    url = Column("URL", String)
    timestamp = Column("Timestamp", DateTime, default=datetime.now)

    def __repr__(self):
        return (
            f"<Instructor(id={self.instructor_id}, "
            f"name={self.full_name}, "
            f"rating={self.rating}, "
            f"url={self.url}, "
            f"timestamp={self.timestamp}, "
        )


class Term(Base):
    __tablename__ = "Term"

    date = Column("Date", Integer, primary_key=True)
    description = Column("Description", String, primary_key=True)

    def __repr__(self):
        return f"<Term(date={self.date}, " f"description={self.description}>"
