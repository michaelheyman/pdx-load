from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database import Base


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
