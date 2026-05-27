import time
import json

from datetime import datetime

from sqlalchemy.orm import Session

from app.workers.celery_app import celery

from app.core.database import SessionLocal

from app.models.task import Task


@celery.task
def simulate_ml_task(task_id: str):

    db: Session = SessionLocal()

    try:

        task = db.query(Task).filter(
            Task.task_id == task_id
        ).first()

        if not task:

            raise Exception(
                f"Task {task_id} not found in database"
            )

        task.status = "PROCESSING"

        db.commit()

        time.sleep(10)

        fake_result = {
            "summary": "Fake ML inference completed",
            "model": "rag-document-analyzer",
            "processing_time_ms": 10000
        }

        task.status = "SUCCESS"

        task.result = json.dumps(
            fake_result
        )

        task.completed_at = datetime.utcnow()

        db.commit()

        return fake_result

    except Exception as e:

        task = db.query(Task).filter(
            Task.task_id == task_id
        ).first()

        if task:

            task.status = "FAILED"

            task.error = str(e)

            db.commit()

        raise e

    finally:

        db.close()