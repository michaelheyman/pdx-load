from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from app.database import dal


class Instructor(dal.Base):
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
