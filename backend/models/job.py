from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func  # for using the now() function

from db.database import Base  # data model 'story' will inherit from class BASE

# JOB is going to represent the intent to make a story
# JOB TELLS US STATUS OF STORY CREATION
# frontend sends the job and then backend received the job

# frontend - ask if job is done ?
# backend - report status ( whether in progress / completed )
#       if job is done , backend send the story to frontend

class StoryJob(Base):
    __tablename__ = "story_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True, unique=True)
    session_id = Column(String, index=True)
    theme = Column(String)
    status = Column(String)
    story_id = Column(Integer, nullable=True) # nullable means value should be null / empty
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Error occurred while testing the API
    # getting null value for completed_at
    # changing completed_job to completed_at
    # NOTE : WHEN CHANGING COLUMN NAMES IN DATA MODELS, MAKE SURE TO DELETE THE database.db older version or else
    # FASTApi will keep on taking the older column name as it is stored in the catching location
    # After deleting it - run API again and new database.db file will be created with the changed column name



