import pytest
from mechanics import roll_d20, roll_boon, roll_bane, calculate_outcome, Outcome

def test_roll_d20_bounds():
    """Verify d20 rolls are within [1, 20]."""
    for _ in range(100):
        val = roll_d20()
        assert 1 <= val <= 20

def test_roll_boon_counts():
    """Verify boon dice scale appropriately with stacks."""
    # 0 stacks should be 0
    assert roll_boon(0) == 0
    # 1 stack (d4)
    for _ in range(20):
        assert 1 <= roll_boon(1) <= 4
    # 5+ stacks (d12)
    for _ in range(20):
        assert 1 <= roll_boon(5) <= 12
        assert 1 <= roll_boon(10) <= 12

def test_calculate_outcome():
    """Verify outcome logic based on DT and roll totals."""
    # DT 12
    # Clean Success (DT + 3)
    assert calculate_outcome(15, 12) == Outcome.CLEAN_SUCCESS
    assert calculate_outcome(20, 12) == Outcome.CLEAN_SUCCESS
    
    # Setback (Within 2 of DT)
    assert calculate_outcome(12, 12) == Outcome.SETBACK
    assert calculate_outcome(11, 12) == Outcome.SETBACK
    assert calculate_outcome(13, 12) == Outcome.SETBACK
    assert calculate_outcome(10, 12) == Outcome.SETBACK
    assert calculate_outcome(14, 12) == Outcome.SETBACK
    
    # Failure (Below DT - 2)
    assert calculate_outcome(5, 12) == Outcome.FAILURE
    
    # Catastrophe (DT - 10)
    assert calculate_outcome(2, 12) == Outcome.CATASTROPHE
    assert calculate_outcome(1, 12) == Outcome.CATASTROPHE

def test_outcome_edge_cases():
    """Check boundaries of outcome calculation."""
    # Setback is [dt-2, dt+2] -> [10, 14] for DT 12
    assert calculate_outcome(9, 12) == Outcome.FAILURE
    assert calculate_outcome(15, 12) == Outcome.CLEAN_SUCCESS
