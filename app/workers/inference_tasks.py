import time
import json

from datetime import datetime

from sqlalchemy.orm import Session

from app.workers.celery_app import celery

from app.core.database import SessionLocal

from app.models.task import Task


@celery.task
def simulate_ml_task(
    task_id: str,
    pipeline_name: str
):

    db: Session = SessionLocal()

    try:

        task = db.query(Task).filter(
            Task.task_id == task_id
        ).first()

        if not task:

            raise Exception(
                f"Task {task_id} not found"
            )

        task.status = "PROCESSING"

        db.commit()

        if pipeline_name == "basic-document-summary":

            time.sleep(5)

            fake_result = {

                "pipeline": (
                    "basic-document-summary"
                ),

                "summary": (
                    "Generated lightweight "
                    "document summary"
                ),

                "pages_processed": 12,

                "processing_time_ms": 5000
            }

        elif pipeline_name == "enterprise-rag-analysis":

            time.sleep(15)

            fake_result = {

                "pipeline": (
                    "enterprise-rag-analysis"
                ),

                "summary": (
                    "Enterprise RAG analysis "
                    "completed successfully"
                ),

                "retrieved_chunks": 48,

                "vector_search_matches": 12,

                "entities_detected": [
                    "Amazon",
                    "Revenue",
                    "AWS"
                ],

                "processing_time_ms": 15000
            }

        else:

            raise Exception(
                "Invalid pipeline"
            )

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