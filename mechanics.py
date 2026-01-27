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

def roll_bane(stacks: int) -> int:
    """
    Rolls a bane die based on stacks.
    1 stack -> d4
    2 stacks -> d6
    3 stacks -> d8
    4 stacks -> d10
    5+ stacks -> d12
    Returns the result of the roll. Returns 0 if stacks <= 0.
    """
    if stacks <= 0:
        return 0
    elif stacks == 1:
        return random.randint(1, 4)
    elif stacks == 2:
        return random.randint(1, 6)
    elif stacks == 3:
        return random.randint(1, 8)
    elif stacks == 4:
        return random.randint(1, 10)
    else:
        return random.randint(1, 12)

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

def resolve_roll(expertise: bool, aptitude: int, bane_stacks: int, dt: int) -> Tuple[int, bool, Outcome, int, int, int]:
    """
    Performs the full resolution: roll (d20 or 2d20kh) + aptitude + boon - bane_roll vs DT.
    Returns (total, nat20_flag, outcome, die_roll, boon_roll, bane_roll)
    """
    die_roll = roll_d20(expertise=expertise)
    boon_roll = roll_boon()
    bane_roll = roll_bane(bane_stacks)
    
    # Calculate regular total
    total = die_roll + aptitude + boon_roll - bane_roll
    
    # Determine Outcome
    # Nat 20 is a Triumph
    if die_roll == 20:
        outcome = Outcome.TRIUMPH
    else:
        outcome = calculate_outcome(total, dt)
        
    return total, die_roll == 20, outcome, die_roll, boon_roll, bane_roll
