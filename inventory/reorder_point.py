def calculate_reorder_point(avg_daily_demand: float, lead_time_days: int, safety_stock: int) -> dict:
    """
    Calculate Reorder Point (ROP).
    Formula: (Average Daily Demand * Lead Time in Days) + Safety Stock
    """
    if lead_time_days < 0 or avg_daily_demand < 0 or safety_stock < 0:
        raise ValueError("Demand, Lead Time, and Safety Stock cannot be negative.")
        
    rop = (avg_daily_demand * lead_time_days) + safety_stock
    
    return {
        "reorder_point": round(rop, 2),
        "trigger_action": "Purchase Order Required" if rop > 0 else "No Reorder Needed"
    }
