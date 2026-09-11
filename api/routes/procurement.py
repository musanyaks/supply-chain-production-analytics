from fastapi import APIRouter, HTTPException
from api.models.schemas import SupplierScorecardRequest
from procurement.supplier_scorecard import calculate_supplier_scorecard

router = APIRouter()

@router.post("/procurement/supplier-scorecard")
def get_scorecard(req: SupplierScorecardRequest):
    try:
        result = calculate_supplier_scorecard(req.on_time_delivery, req.quality_acceptance, req.cost_competitiveness)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
