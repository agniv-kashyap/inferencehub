import uuid

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.schemas.inference import (
    InferenceRequest,
    InferenceResponse
)

from app.services.task_service import create_task

from app.api.dependencies.rate_limiter import (
    rate_limit_dependency
)

from app.workers.inference_tasks import (
    simulate_ml_task
)

from app.core.pipelines import PIPELINES

router = APIRouter()


@router.post(
    "/infer",
    response_model=InferenceResponse
)
async def infer(
    request: InferenceRequest,
    db: Session = Depends(get_db),
    api_key=Depends(rate_limit_dependency)
):

    pipeline_name = request.pipeline

    pipeline = PIPELINES.get(
        pipeline_name
    )

    if not pipeline:

        raise HTTPException(
            status_code=404,
            detail="Pipeline not found"
        )

    required_tier = pipeline[
        "required_tier"
    ]

    user_tier = api_key.tier

    if (
        required_tier == "premium"
        and user_tier != "premium"
    ):

        raise HTTPException(
            status_code=403,
            detail=(
                "Premium tier required "
                "for this pipeline"
            )
        )

    generated_task_id = str(
        uuid.uuid4()
    )

    create_task(
        db=db,
        task_id=generated_task_id,
        developer_email=api_key.developer_email
    )

    simulate_ml_task.delay(
        generated_task_id,
        pipeline_name
    )

    return {
        "task_id": generated_task_id,
        "status": "PENDING"
    }