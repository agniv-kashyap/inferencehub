import uuid

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.schemas.inference import InferenceResponse

from app.services.task_service import create_task

from app.api.dependencies.rate_limiter import (
    rate_limit_dependency
)

from app.workers.inference_tasks import (
    simulate_ml_task
)

router = APIRouter()


@router.post(
    "/infer",
    response_model=InferenceResponse
)
async def infer(
    db: Session = Depends(get_db),
    api_key=Depends(rate_limit_dependency)
):

    generated_task_id = str(uuid.uuid4())

    create_task(
        db=db,
        task_id=generated_task_id
    )

    simulate_ml_task.delay(
        generated_task_id
    )

    return {
        "task_id": generated_task_id,
        "status": "PENDING"
    }