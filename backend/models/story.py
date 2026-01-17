from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func  # for using the now() function
from sqlalchemy.orm import relationship

from db.database import Base  # data model 'story' will inherit from class BASE
#   Think of it like a Book and its Pages:

#   The Story class is the Book.
# nodes = relationship(...) lets you call book.nodes and get all the Pages inside that book.

# The StoryNode class is a single Page.
# story = relationship(...) lets you call page.story and find out which Book that page belongs to.

# This creates a One-to-Many relationship: One Story can have Many StoryNodes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         'This creates a One-to-Many relationship: One Story can have Many StoryNodes.)
# defining SQL models through sqlalchemy
class Story(Base):   # contains the metadata of the story as a whole
    __tablename__ = 'stories'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    session_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    nodes = relationship("StoryNode",back_populates="story")  # from creating relationship with diff piece of data


class StoryNode(Base):
    __tablename__ = 'story_nodes'

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey('stories.id'), index=True)
    content = Column(String)
    is_root = Column(Boolean, default=False)  # for node which is root - start of the story
    is_ending = Column(Boolean, default=False) # end node
    is_winning = Column(Boolean, default=False) # winning node
    options = Column(JSON, default=list)

    story = relationship("Story", back_populates="nodes")


