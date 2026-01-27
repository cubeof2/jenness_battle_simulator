import logging
from typing import Any
from strategies import random_strategy

logger = logging.getLogger(__name__)

class NPC:
    def __init__(self, name: str, hp: int, dt: int, expertise_attack: bool = False, expertise_defense: bool = False, targeting_strategy=random_strategy):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.dt = dt
        self.expertise_attack = expertise_attack
        self.expertise_defense = expertise_defense
        self.aptitude = 0 # NPCs might not use aptitude if they don't roll, but keeping for compatibility if needed
        self.targeting_strategy = targeting_strategy

    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp < 0: self.hp = 0
        logger.debug(f"{self.name} takes {amount} damage. HP: {self.hp}")

    def is_alive(self) -> bool:
        return self.hp > 0
