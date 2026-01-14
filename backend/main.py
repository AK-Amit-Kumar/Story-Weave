from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

from routers import story,job   # for connecting the routers to the main page
from db.database import create_tables # for creating tables - for storing our stories

create_tables()  # for creating table before spinning up our API


app = FastAPI(
    title="StoryWeave API",
    description="api to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,   # allowing api to be used from different origin - cross origin resource sharing
    allow_origins=settings.ALLOWED_ORIGINS, # from core.config
    allow_credentials=True,  #allow someone to send the credential to backend
    allow_methods=["*"],   # allowing api type methods
    allow_headers=["*"],  # additional info sent with the headers
)

# including routers in the main page
app.include_router(story.router, prefix=settings.API_PREFIX)

app.include_router(job.router, prefix=settings.API_PREFIX)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    # uvicorn - web server which runs the FASTApi application