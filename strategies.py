import random
from typing import List, Optional, Protocol, Any

# Using Any for combatants to avoid circular imports for now, 
# or we can use generic T with bound using Protocol if we want to be strict.
# For simplicity in this script, Any or Object is fine, but we'll try to be clear.

class Combatant(Protocol):
    name: str
    dt: int
    def is_alive(self) -> bool: ...

def get_living_members(team: List[Any]) -> List[Any]:
    return [m for m in team if m.is_alive()]

def lowest_dt_strategy(attacker: Any, enemy_team: List[Any]) -> Optional[Any]:
    """Target the enemy with the lowest Difficulty Threshold (DT)."""
    living_enemies = get_living_members(enemy_team)
    if not living_enemies:
        return None
    # Sort by DT, then random index for tie breaking (stable sort)
    living_enemies.sort(key=lambda x: x.dt)
    return living_enemies[0]

def random_strategy(attacker: Any, enemy_team: List[Any]) -> Optional[Any]:
    """Target a random living enemy."""
    living_enemies = get_living_members(enemy_team)
    if not living_enemies:
        return None
    return random.choice(living_enemies)
