import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.services.task_service import (
    get_task,
    get_tasks_for_user
)

from app.api.dependencies.auth import (
    validate_api_key
)

router = APIRouter()


@router.get("/tasks")
async def list_user_tasks(
    db: Session = Depends(get_db),
    api_key=Depends(validate_api_key)
):

    tasks = get_tasks_for_user(
        db=db,
        developer_email=api_key.developer_email
    )

    response = []

    for task in tasks:

        parsed_result = None

        if task.result:

            parsed_result = json.loads(
                task.result
            )

        response.append({

            "task_id": task.task_id,

            "status": task.status,

            "result": parsed_result,

            "error": task.error,

            "created_at": task.created_at,

            "completed_at": task.completed_at
        })

    return response


@router.get("/tasks/{task_id}")
async def get_task_status(
    task_id: str,
    db: Session = Depends(get_db),
    api_key=Depends(validate_api_key)
):

    task = get_task(
        db=db,
        task_id=task_id
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if (
        task.developer_email
        != api_key.developer_email
    ):

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    parsed_result = None

    if task.result:

        parsed_result = json.loads(
            task.result
        )

    return {

        "task_id": task.task_id,

        "status": task.status,

        "result": parsed_result,

        "error": task.error,

        "created_at": task.created_at,

        "completed_at": task.completed_at
    }