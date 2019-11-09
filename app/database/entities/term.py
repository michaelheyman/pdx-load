from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database import Base


class Term(Base):
    __tablename__ = "Term"

    date = Column("Date", Integer, primary_key=True)
    description = Column("Description", String, primary_key=True)

    def __repr__(self):
        return f"<Term(date={self.date}, " f"description={self.description}>"
