from pydantic import BaseModel, Field

class EOQRequest(BaseModel):
    annual_demand: float = Field(..., gt=0, description="Total annual demand in units")
    ordering_cost: float = Field(..., gt=0, description="Cost to place one order")
    holding_cost: float = Field(..., gt=0, description="Holding cost per unit per year")

class ROPRequest(BaseModel):
    avg_daily_demand: float = Field(..., ge=0)
    lead_time_days: int = Field(..., ge=0)
    safety_stock: int = Field(..., ge=0)

class SupplierScorecardRequest(BaseModel):
    on_time_delivery: float = Field(..., ge=0, le=100)
    quality_acceptance: float = Field(..., ge=0, le=100)
    cost_competitiveness: float = Field(..., ge=0, le=100)

class OEERequest(BaseModel):
    availability: float = Field(..., ge=0, le=1)
    performance: float = Field(..., ge=0, le=1)
    quality: float = Field(..., ge=0, le=1)
