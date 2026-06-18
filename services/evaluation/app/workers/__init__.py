from app.workers.celery import celery_app
# Import tasks so they are registered with the Celery app instance
from app.workers.tasks import run_ragas_evaluation

__all__ = ["celery_app", "run_ragas_evaluation"]
