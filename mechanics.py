import random
from enum import Enum
from typing import Tuple

class Outcome(Enum):
    """Enumeration of possible roll outcomes."""
    TRIUMPH = "Triumph"
    CLEAN_SUCCESS = "Clean Success"
    SETBACK = "Setback"
    FAILURE = "Failure"
    CATASTROPHE = "Catastrophe"

def roll_d20(expertise: bool = False) -> int:
    """
    Rolls a d20. If expertise is True, rolls 2d20 and keeps the highest.
    
    Args:
        expertise (bool): If True, grant advantage (2d20kh).
        
    Returns:
        int: The result of the roll.
    """
    if expertise:
        r1 = random.randint(1, 20)
        r2 = random.randint(1, 20)
        return max(r1, r2)
    return random.randint(1, 20)

def roll_boon() -> int:
    """
    Rolls a 1d4 boon.
    
    Returns:
        int: Result (1-4).
    """
    return random.randint(1, 4)

def roll_bane(stacks: int) -> int:
    """
    Rolls a bane die based on number of stacks.
    
    Scaling:
    - 1 stack: d4
    - 2 stacks: d6
    - 3 stacks: d8
    - 4 stacks: d10
    - 5+ stacks: d12
    
    Args:
        stacks (int): The number of bane stacks accumulated.
        
    Returns:
        int: The result of the bane die roll. Returns 0 if stacks <= 0.
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
    """
    Determines the outcome based on roll total and difficulty threshold.
    
    Rules:
    - Total >= DT+3: Clean Success
    - Total >= DT-2: Setback (Success with complications, or Failure with bonus?) 
      (Note: Historically Setback usually means Failure but close, or Success with consequence. 
       In this engine Setback often results in Failure/Momentum loss but minimal bad stuff.)
    - Total <= DT-10: Catastrophe
    - Otherwise: Failure
    
    Args:
        roll_total (int): The final calculated total of the roll.
        dt (int): The difficulty threshold to beat.
        
    Returns:
        Outcome: The result enum.
    """
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
    Performs the full resolution mechanics: 
    1. Roll d20 (or 2d20kh if expert).
    2. Add Aptitude.
    3. Add Boon (d4).
    4. Subtract Bane (d4-d12 based on stacks).
    5. Compare to DT.
    
    Args:
        expertise (bool): If True, use advantageous d20 roll.
        aptitude (int): Base bonus to add.
        bane_stacks (int): Number of banes to determine bane die size.
        dt (int): Difficulty Threshold.
        
    Returns:
        Tuple containing:
        - total (int): Final calculated value.
        - nat20 (bool): True if the d20 roll was a natural 20.
        - outcome (Outcome): The result enum.
        - die_roll (int): The raw d20 roll result.
        - boon_roll (int): The raw boon roll result.
        - bane_roll (int): The raw bane roll result.
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

