from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# CUSTOM CAKE SHOP ANALOGY FOR DATA SCHEMA:
#
# | Schema Class     | Analogy                  | Description/Role in Workflow                                                                  |
# | ---------------- | ------------------------ | --------------------------------------------------------------------------------------------- |
# | StoryJobBase     | The Flavor Profile       | Defines the *minimum* required data (e.g., the story theme) for *any* job request.            |
# | StoryJobCreate   | The Order Slip           | Used specifically for *creating* a new job request. It inherits required fields from StoryJobBase. |
# | StoryJobResponse | The Tracking ID/Receipt  | Used to *track* the job's progress. Includes status, timestamps, and optional fields for the final result (story_id) or an error. |

class StoryJobBase(BaseModel): # will be used with other job schema
    theme: str

# Error Resolution: Error --> Validation Error ( Input should be an integer )
# Understanding: In routers\job.py - job_id was used as str but schemas\job have job_id declared as int
# Improvement : declared job_is attribute as str
class StoryJobResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    story_id: Optional[int] = None  # Optional means we will get this if certain condition is met
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True

# functionality of both classes are same, but below one will be used as Request
class StoryJobCreate(StoryJobBase): # inheriting from StoryJobBase
    pass