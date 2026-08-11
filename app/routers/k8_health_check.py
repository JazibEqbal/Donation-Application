from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def liveness():
    return {
        "status": "ok"
    }


@router.get("/ready")
def readiness():
    return {
        "status": "ready"
    }