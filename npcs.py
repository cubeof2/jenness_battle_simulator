import logging
from typing import Any
from mechanics import Combatant
from strategies import random_strategy

logger = logging.getLogger(__name__)

class NPC:
    """Represents a Non-Player Character (Enemy).
    
    Attributes:
        name: The display name of the NPC.
        hp: Current Hit Points.
        max_hp: Maximum Hit Points.
        dt: Difficulty Threshold (Defense Class) players must beat.
        expertise_attack: If True, imposes a Bane on PC Defense rolls.
        expertise_defense: If True, imposes a Bane on PC Attack rolls.
        targeting_strategy: Function to select a target from a list of enemies.
    """
    def __init__(
        self, 
        name: str, 
        hp: int, 
        dt: int, 
        expertise_attack: bool = False, 
        expertise_defense: bool = False, 
        targeting_strategy: Any = random_strategy
    ):
        """Initializes an NPC.

        Args:
            name: Name of the NPC.
            hp: Hit points.
            dt: Difficulty Threshold.
            expertise_attack: Whether the NPC has attack expertise.
            expertise_defense: Whether the NPC has defense expertise.
            targeting_strategy: Strategy function for targeting.
        """
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.dt = dt
        self.expertise_attack = expertise_attack
        self.expertise_defense = expertise_defense
        self.targeting_strategy = targeting_strategy

    def take_damage(self, amount: int):
        """
        Apply damage to the NPC.

        Args:
            amount (int): Amount of damage to subtract from HP.
        """
        self.hp -= amount
        if self.hp < 0: self.hp = 0
        logger.debug(f"{self.name} takes {amount} damage. HP: {self.hp}")

    def is_alive(self) -> bool:
        """
        Check if the NPC is alive.

        Returns:
            bool: True if HP > 0, False otherwise.
        """
        return self.hp > 0
