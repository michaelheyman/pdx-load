from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import config


engine = create_engine(f"sqlite:///{config.DATABASE_PATH}", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
DBSession = Session()


def initialize_database():
    Base.metadata.create_all(engine)
