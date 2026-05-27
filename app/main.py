from fastapi import FastAPI

from app.core.database import Base
from app.core.database import engine

from app.models.task import Task
from app.models.api_key import APIKey

from app.api.routes.inference import (
    router as inference_router
)

from app.api.routes.tasks import (
    router as task_router
)

from app.api.routes.auth import (
    router as auth_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)

app.include_router(inference_router)

app.include_router(task_router)


@app.get("/")
async def root():

    return {
        "message": "InferenceHub API Running"
    }