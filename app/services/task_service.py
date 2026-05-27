from sqlalchemy.orm import Session

from app.models.task import Task


def create_task(
    db: Session,
    task_id: str,
    developer_email: str
):

    task = Task(
        task_id=task_id,
        developer_email=developer_email,
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


def get_tasks_for_user(
    db: Session,
    developer_email: str
):

    return db.query(Task).filter(
        Task.developer_email == developer_email
    ).order_by(
        Task.created_at.desc()
    ).all()