from fastapi import APIRouter, HTTPException
from api.models.schemas import EOQRequest, ROPRequest
from inventory.eoq import calculate_eoq
from inventory.reorder_point import calculate_reorder_point

router = APIRouter()

@router.post("/inventory/eoq")
def get_eoq(req: EOQRequest):
    try:
        result = calculate_eoq(req.annual_demand, req.ordering_cost, req.holding_cost)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/inventory/reorder-point")
def get_rop(req: ROPRequest):
    try:
        result = calculate_reorder_point(req.avg_daily_demand, req.lead_time_days, req.safety_stock)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
