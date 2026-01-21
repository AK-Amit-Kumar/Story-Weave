import uuid  # for generating unique id for story
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal

from models.story import Story, StoryNode
from models.job import StoryJob

from schemas.story import (
    CompleteStoryResponse, CompleteStoryNodeResponse, CreateStoryRequest, StoryOptionsSchema
)
from schemas.job import StoryJobResponse
from core.story_generator import StoryGenerator

# here we are going create endpoints that will be
# hit by the user

# below router will allow to create diff endpoints in diff files
# and also API prefixes for them
router = APIRouter(
    prefix="/stories",
    tags=["Stories"],  # for documentation purpose
)

# eg for backend url having this routing
#     --> backend_url/api/stories/endpoint
#  - specific url we will hit
# Session : It will identify in browse when we are interacting with a website

# for getting session id and creating session id if not available
def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

# creating different endpoints
# for creating something new
@router.post("/create", response_model=StoryJobResponse)
def create_story(
        request: CreateStoryRequest,
        background_tasks: BackgroundTasks,  # for running independently of the main thread
        response: Response,
        session_id: str = Depends(get_session_id),  # injecting value from get session id function into parameter of this function
        db: Session = Depends(get_db)
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)  # for storing the session id - it is not that secure as user can see this

    # We will generate new JOb id now
    # when user want to create the story -> Actually a job will be created
    # -> that will trigger a background task to run -> go to OpenAI to call LLM
    # which will then make our story

    job_id = str(uuid.uuid4())

    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="pending"
    )
    # adding the job in the database
    db.add(job)
    db.commit()  # for saving it in db - job of Object relational mappinf ORM

    # using background task , it will run generate_story_task in the background
    # generating the story might take time but as it will run in the background, it will
    # not disturb the flow of running API
    background_tasks.add_task(
        generate_story_task,
        job_id=job_id,
        theme=request.theme,
        session_id=session_id
    )

    return job

def generate_story_task(job_id: str, theme: str, session_id: str):
    db = SessionLocal()  # for creating separate db sessions

    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

        if not job:
            return

        try:
            job.status = "processing"
            db.commit()

            # calling Story generator .py file and storing it in "story" dict
            story = StoryGenerator.generate_story(db, session_id, theme) # generate story

            job.story_id = story.id  #update story id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()

        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()

    finally:
        db.close()


# ENDPOINT TO RETRIEVE THE CREATED STORY
#   {story_id} path parameter should be same as used in function parameter
@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    # Checking whether story which we are trying to receive exist in the db or NOT
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # parsing story - building the story in frontend acceptable format
    complete_story = build_complete_story_tree(db, story)
    return complete_story


def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    #fetching all the nodes created in the DB using story_generator
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    #using fetched nodes data from db and create a tree that can be sent to frontend
    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,   # replacing is_winning_ending with is_winning
            options=node.options
        )

        node_dict[node.id] = node_response

    # fetching root node
    #next() - it iterates on the iterable object and check based on the condition
    root_node = next((node for node in nodes if node.is_root), None)

    if not root_node:
        raise HTTPException(status_code=500, detail="Story root node not found")

    return CompleteStoryResponse(
        id=story.id,
        title=story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )








