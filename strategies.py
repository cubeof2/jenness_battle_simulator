import random
from typing import List, Optional
from mechanics import Combatant

def random_strategy(actor: Combatant, enemy_team: List[Combatant]) -> Optional[Combatant]:
    """
    Randomly selects a target from the living enemies.
    
    Args:
        actor (Any): The entity acting.
        enemy_team (List[Any]): List of enemy entities.
        
    Returns:
        Optional[Any]: The selected target, or None.
    """
    living_enemies = [e for e in enemy_team if e.is_alive()]
    if not living_enemies:
        return None
    return random.choice(living_enemies)

def lowest_dt_strategy(actor: Combatant, enemy_team: List[Combatant]) -> Optional[Combatant]:
    """
    Selects the enemy with the lowest Difficulty Threshold (DT).
    
    Args:
        actor (Any): The entity acting.
        enemy_team (List[Any]): List of enemy entities.
        
    Returns:
        Optional[Any]: The selected target, or None.
    """
    living_enemies = [e for e in enemy_team if e.is_alive()]
    if not living_enemies:
        return None
    
    # Check if enemy has DT
    candidates = [e for e in living_enemies if hasattr(e, 'dt')]
    if not candidates:
        # If no candidates have 'dt', fall back to random selection from all living enemies
        return random.choice(living_enemies)
        
    return min(candidates, key=lambda x: x.dt)
