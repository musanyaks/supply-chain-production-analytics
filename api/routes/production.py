from fastapi import APIRouter, HTTPException
from api.models.schemas import OEERequest
from production.production_efficiency import calculate_oee

router = APIRouter()

@router.post("/production/oee")
def get_oee(req: OEERequest):
    try:
        result = calculate_oee(req.availability, req.performance, req.quality)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
