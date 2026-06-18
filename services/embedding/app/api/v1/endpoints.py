from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Form
from app.pipeline.pipeline import EmbeddingPipeline
from app.schemas.document import PipelineConfig
from pydantic import BaseModel
import json

router = APIRouter()

class IngestRequest(BaseModel):
    doc_id: str
    content: str
    filename: str
    tenant_id: str
    config: PipelineConfig = PipelineConfig()

@router.get("/health")
async def health():
    return {"status": "healthy"}

@router.post("/ingest")
async def trigger_ingestion(req: IngestRequest, background_tasks: BackgroundTasks):
    pipeline = EmbeddingPipeline()
    background_tasks.add_task(
        pipeline.ingest,
        doc_id=req.doc_id,
        content=req.content.encode('utf-8'),
        filename=req.filename,
        tenant_id=req.tenant_id,
        config=req.config
    )
    return {"message": "Ingestion task triggered successfully"}

@router.post("/ingest-file")
async def trigger_file_ingestion(
    background_tasks: BackgroundTasks,
    tenant_id: str = Form(...),
    doc_id: str = Form(...),
    file: UploadFile = File(...),
    config: str = Form(None)  # Optional JSON string for PipelineConfig
):
    pipeline_config = PipelineConfig()
    if config:
        try:
            config_dict = json.loads(config)
            pipeline_config = PipelineConfig(**config_dict)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid config JSON: {e}")
            
    content = await file.read()
    pipeline = EmbeddingPipeline()
    
    background_tasks.add_task(
        pipeline.ingest,
        doc_id=doc_id,
        content=content,
        filename=file.filename,
        tenant_id=tenant_id,
        config=pipeline_config
    )
    return {
        "message": "File ingestion task triggered successfully",
        "filename": file.filename,
        "doc_id": doc_id
    }

