import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from production.production_efficiency import calculate_oee

def test_oee_calculation():
    # 0.85 * 0.90 * 0.95 = 0.72675 -> 72.67 (due to Python float rounding)
    result = calculate_oee(0.85, 0.90, 0.95)
    assert result['oee_percentage'] == 72.67

def test_oee_invalid_input():
    with pytest.raises(ValueError):
        calculate_oee(1.5, 0.9, 0.9) # Availability > 1
