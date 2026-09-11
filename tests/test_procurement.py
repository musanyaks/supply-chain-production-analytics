import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from procurement.supplier_scorecard import calculate_supplier_scorecard

def test_supplier_tier_strategic():
    result = calculate_supplier_scorecard(95, 95, 95)
    assert result['total_score'] == 95.0
    assert result['tier'] == "Strategic Partner"

def test_supplier_tier_conditional():
    result = calculate_supplier_scorecard(50, 50, 50)
    assert result['total_score'] == 50.0
    assert result['tier'] == "Conditional"
