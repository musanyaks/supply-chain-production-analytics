def calculate_supplier_scorecard(on_time_delivery: float, quality_acceptance: float, cost_competitiveness: float) -> dict:
    """
    Calculates a weighted supplier scorecard.
    Weights: 40% Delivery, 40% Quality, 20% Cost.
    Values should be 0-100.
    """
    if not all(0 <= x <= 100 for x in [on_time_delivery, quality_acceptance, cost_competitiveness]):
        raise ValueError("Metrics must be between 0 and 100.")
        
    score = (on_time_delivery * 0.4) + (quality_acceptance * 0.4) + (cost_competitiveness * 0.2)
    
    if score >= 90:
        tier = "Strategic Partner"
    elif score >= 75:
        tier = "Preferred"
    elif score >= 60:
        tier = "Approved"
    else:
        tier = "Conditional"
        
    return {
        "total_score": round(score, 2),
        "tier": tier
    }
