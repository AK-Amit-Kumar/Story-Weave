from sqlalchemy import create_engine  # engine wrapping around db with which we are interacting
from sqlalchemy.orm import sessionmaker # make session used for making connection with db
from sqlalchemy.ext.declarative import declarative_base # Data models will inherit from this base class - for knowing which data model we have in our databse

from core.config import settings

engine = create_engine(
    settings.DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # data models with inherit from this class so that it can work with our SQL ORM

def get_db():  # give access to db session and make sure there are no multiple session opened at same time
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables(): # this function will create the tables in db based on the data models that we have created when  we will spin up the app
    Base.metadata.create_all(bind=engine)