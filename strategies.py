import random
from typing import List, Any, Optional

# Using Any for combatants to avoid circular imports for now, 
# or we can use generic T with bound using Protocol if we want to be strict.
# For simplicity in this script, Any or Object is fine, but we'll try to be clear.

# The Combatant Protocol and get_living_members helper are removed as they are not used by the new strategies.

def random_strategy(actor: Any, enemy_team: List[Any]) -> Optional[Any]:
    """Randomly selects a target from the living enemies."""
    living_enemies = [e for e in enemy_team if e.is_alive()]
    if not living_enemies:
        return None
    return random.choice(living_enemies)

def lowest_dt_strategy(actor: Any, enemy_team: List[Any]) -> Optional[Any]:
    """Selects the enemy with the lowest DT."""
    living_enemies = [e for e in enemy_team if e.is_alive()]
    if not living_enemies:
        return None
    
    # Check if enemy has DT
    candidates = [e for e in living_enemies if hasattr(e, 'dt')]
    if not candidates:
        # If no candidates have 'dt', fall back to random selection from all living enemies
        return random.choice(living_enemies)
        
    return min(candidates, key=lambda x: x.dt)
