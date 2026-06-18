from fastapi import APIRouter

router = APIRouter(prefix="/users")

@router.get("/health")
async def health():
    return {"status": "healthy"}
