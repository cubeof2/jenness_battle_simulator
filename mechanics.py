import random
from enum import Enum
from typing import Tuple

class Outcome(Enum):
    TRIUMPH = "Triumph"
    CLEAN_SUCCESS = "Clean Success"
    SETBACK = "Setback"
    FAILURE = "Failure"
    CATASTROPHE = "Catastrophe"

def roll_d20(expertise: bool = False) -> int:
    """Rolls a d20. If expertise is True, rolls 2d20 and keeps the highest."""
    if expertise:
        r1 = random.randint(1, 20)
        r2 = random.randint(1, 20)
        return max(r1, r2)
    return random.randint(1, 20)

def roll_boon() -> int:
    """Rolls a 1d4 boon."""
    return random.randint(1, 4)

def calculate_outcome(roll_total: int, dt: int) -> Outcome:
    """Determines the outcome based on roll total and difficulty threshold."""
    if roll_total >= dt + 3:
        return Outcome.CLEAN_SUCCESS 
    elif roll_total >= dt - 2: 
         return Outcome.SETBACK
    elif roll_total <= dt - 10:
        return Outcome.CATASTROPHE
    else:
        return Outcome.FAILURE

def resolve_roll(is_expert: bool, aptitude: int, banes: int, dt: int) -> Tuple[int, bool, Outcome, int, int]:
    """
    Performs the full resolution: roll + bonus - penalty vs DT.
    Returns (total, nat20_flag, outcome, die_roll, boon_roll)
    """
    die_roll = roll_d20(expertise=is_expert)
    boon_roll = roll_boon()
    
    # Calculate regular total
    total = die_roll + aptitude + boon_roll - banes
    
    # Determine Outcome
    if die_roll == 20:
        outcome = Outcome.TRIUMPH
    elif total <= dt - 10:
         outcome = Outcome.CATASTROPHE
    elif total < dt - 2:
        outcome = Outcome.FAILURE
    elif total >= dt + 3:
        outcome = Outcome.CLEAN_SUCCESS
    else:
        # total is between DT-2 and DT+2 inclusive
        outcome = Outcome.SETBACK
        
    return total, die_roll == 20, outcome, die_roll, boon_roll
