import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inventory.eoq import calculate_eoq
from inventory.reorder_point import calculate_reorder_point

def test_eoq_calculation():
    result = calculate_eoq(10000, 50, 2.5)
    assert result['eoq'] == 632.46

def test_eoq_zero_holding_cost():
    with pytest.raises(ValueError):
        calculate_eoq(1000, 50, 0)

def test_rop_calculation():
    result = calculate_reorder_point(30, 7, 50)
    assert result['reorder_point'] == 260
