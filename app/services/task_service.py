from sqlalchemy.orm import Session

from app.models.task import Task


def create_task(
    db: Session,
    task_id: str
):

    task = Task(
        task_id=task_id,
        status="PENDING"
    )

    db.add(task)

    db.commit()

    db.refresh(task)

    return task


def get_task(
    db: Session,
    task_id: str
):

    return db.query(Task).filter(
        Task.task_id == task_id
    ).first()