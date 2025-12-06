from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel


# WE will work python classes that specifies the type of data that api to accept/to return.
# It allows FASTApi to automatically do some data validation for us - ensuring correct data is coming to
# api

# schemas - structure of data that api can expect to get and we can expect api to return

# -------------------------------------------------------------
# PYDANTIC SCHEMA ANALOGY: SANDWICH RECIPE FLOW (CONTROL/DEPENDENCY)
# -------------------------------------------------------------
# Step | Data Schema              | Analogy                    | Relationship
# -----|--------------------------|----------------------------|-----------------------------------------
# 1. Define Atoms | StoryOptionsSchema | Condiment Instructions     | Used by CompleteStoryNodeResponse
# 2. Define Bases | StoryNodeBase      | Base Fillings              | Inherited by CompleteStoryNodeResponse
# 2. Define Bases | StoryBase          | Meal Title                 | Inherited by CompleteStoryResponse
# 3. Assemble Block| CompleteStoryNodeResponse| Complete Layer Recipe      | Used by CompleteStoryResponse
# 4. Final Output | CompleteStoryResponse| Final Meal Plating         | Puts all the blocks together
# -------------------------------------------------------------

# classes which inherit from 'BaseModel' pydantic class
class StoryOptionsSchema(BaseModel): # this class will be used as type in other schema clas
    text: str
    node_id: Optional[int] = None

# naming convention __Base is being used as pairing class which will be used to write othe complex schemas
class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False

# below class inherit from 'StoryNodeBase' class
class CompleteStoryNodeResponse(StoryNodeBase):  # data format of response from out api
    id: int
    options: List[StoryOptionsSchema] = []
    # options is of type 'StoryOptionsSchema' class which was defined earlier

    class Config:
        from_attributes = True

class StoryBase(BaseModel):
    title: str
    session_id: Optional[str] = None

    class Config:
        from_attributes = True

class CreateStoryRequest(BaseModel):
    theme: str

class CompleteStoryResponse(StoryBase):
    id: int
    created_at: datetime
    root_node: CompleteStoryNodeResponse
    all_nodes: Dict[int, CompleteStoryNodeResponse]

    class Config:
        from_attributes = True




