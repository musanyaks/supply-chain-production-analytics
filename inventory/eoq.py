import math

def calculate_eoq(annual_demand: float, ordering_cost: float, holding_cost: float) -> dict:
    """
    Calculate Economic Order Quantity (EOQ).
    Formula: sqrt((2 * D * S) / H)
    """
    if holding_cost <= 0 or annual_demand < 0 or ordering_cost < 0:
        raise ValueError("Demand, Ordering Cost, and Holding Cost must be positive numbers.")
    
    eoq = math.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
    
    return {
        "eoq": round(eoq, 2),
        "annual_demand": annual_demand,
        "ordering_cost": ordering_cost,
        "holding_cost": holding_cost
    }
