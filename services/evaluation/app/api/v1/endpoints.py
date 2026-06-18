from fastapi import APIRouter
from app.workers.tasks import run_ragas_evaluation
from pydantic import BaseModel

router = APIRouter()

class EvalRequest(BaseModel):
    evaluation_run_id: str

@router.get("/health")
async def health():
    return {"status": "healthy"}

@router.post("/evaluate")
async def trigger_evaluation(req: EvalRequest):
    # Queue the evaluation task using delay()
    task = run_ragas_evaluation.delay(req.evaluation_run_id)
    return {
        "message": "Evaluation run queued successfully",
        "task_id": task.id
    }
