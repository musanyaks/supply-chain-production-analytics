def calculate_oee(availability: float, performance: float, quality: float) -> dict:
    """
    Calculates Overall Equipment Effectiveness (OEE).
    Values should be passed as decimals (e.g., 0.85 for 85%).
    """
    if not all(0 <= x <= 1 for x in [availability, performance, quality]):
        raise ValueError("All inputs must be between 0 and 1.")
        
    oee = availability * performance * quality
    
    return {
        "oee_percentage": round(oee * 100, 2),
        "availability_loss": round((1 - availability) * 100, 2),
        "performance_loss": round((1 - performance) * 100, 2),
        "quality_loss": round((1 - quality) * 100, 2)
    }
