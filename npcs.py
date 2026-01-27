import logging
from typing import Any
from strategies import random_strategy

logger = logging.getLogger(__name__)

class NPC:
    """
    Represents a Non-Player Character (Enemy).
    
    Attributes:
        name (str): The name of the NPC.
        hp (int): Current Hit Points.
        max_hp (int): Maximum Hit Points.
        dt (int): Difficulty Threshold (Defense Class).
        expertise_attack (bool): If True, imposes a Bane on PC Defense rolls.
        expertise_defense (bool): If True, imposes a Bane on PC Attack rolls.
        targeting_strategy (callable): Function to select a target from a list of enemies.
    """
    def __init__(self, name: str, hp: int, dt: int, expertise_attack: bool = False, expertise_defense: bool = False, targeting_strategy=random_strategy):
        """
        Initialize an NPC.

        Args:
            name (str): Name of the NPC.
            hp (int): Hit points.
            dt (int): Difficulty Threshold.
            expertise_attack (bool, optional): Whether the NPC has attack expertise. Defaults to False.
            expertise_defense (bool, optional): Whether the NPC has defense expertise. Defaults to False.
            targeting_strategy (callable, optional): Strategy function for targeting. Defaults to random_strategy.
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
