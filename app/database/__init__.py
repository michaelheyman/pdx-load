from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import config


class DataAccessLayer:
    # https://www.oreilly.com/library/view/essential-sqlalchemy-2nd/9781491916544/ch04.html
    Base = declarative_base()
    conn_string = f"sqlite:///{config.DATABASE_FILE}"
    connection = None
    engine = None
    Session = None
    DBSession = None

    def db_init(self, conn_string=None):
        self.engine = create_engine(conn_string or self.conn_string, echo=False)
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.DBSession = self.Session()


dal = DataAccessLayer()
