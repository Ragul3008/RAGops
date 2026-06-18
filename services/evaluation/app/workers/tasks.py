from app.workers.celery import celery_app
from app.evaluators.ragas_evaluator import RAGASEvaluator
from app.evaluators.hallucination_detector import (
    HallucinationDetector
)

# Helper stubs for missing functions
def fetch_eval_samples(run_id: str) -> list:
    return []

def save_eval_result(run_id: str, result) -> None:
    pass

def publish_event(event_name: str, payload: dict) -> None:
    pass

@celery_app.task(
    name="evaluation.run_ragas",
    bind=True,
    max_retries=3,
    acks_late=True,
)
def run_ragas_evaluation(
    self, evaluation_run_id: str
):
    try:
        evaluator = RAGASEvaluator()
        samples = fetch_eval_samples(evaluation_run_id)
        result = evaluator.evaluate(samples)
        save_eval_result(evaluation_run_id, result)
        publish_event("evaluation.completed", {
            "run_id": evaluation_run_id,
            "scores": result.dict(),
        })
    except Exception as exc:
        self.retry(exc=exc, countdown=60)