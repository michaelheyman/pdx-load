from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database import dal


class ClassOffering(dal.Base):
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
