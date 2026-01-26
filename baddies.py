from mechanics import resolve_roll, Outcome
import logging
from typing import Any
from strategies import random_strategy

logger = logging.getLogger(__name__)

class Baddies:
    def __init__(self, name: str, hp: int, dt: int, expertise_attack: bool = False, expertise_defense: bool = False, targeting_strategy=random_strategy):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.dt = dt
        self.expertise_attack = expertise_attack
        self.expertise_defense = expertise_defense
        self.aptitude = 0 
        self.targeting_strategy = targeting_strategy

    def make_attack(self, target: Any, banes: int) -> tuple[int, Outcome]:
        logger.debug(f"{self.name} attacks {target.name}!")
        
        total, nat20, outcome, die_roll, boon_roll = resolve_roll(self.expertise_attack, self.aptitude, banes, target.dt)
        
        logger.debug(f"  -> Attack Roll: {die_roll} (d20) + {self.aptitude} (Apt) + {boon_roll} (Boon) - {banes} (Banes) = {total}")
        logger.debug(f"  -> vs DT {target.dt}: {outcome.value}")

        damage = 0
        if outcome == Outcome.TRIUMPH:
            damage = 2
        elif outcome == Outcome.CLEAN_SUCCESS:
             damage = 1
        
        return damage, outcome

    def make_defense(self, attacker_dt: int, banes: int) -> Outcome:
         total, nat20, outcome, die_roll, boon_roll = resolve_roll(self.expertise_defense, self.aptitude, banes, attacker_dt)
         logger.debug(f"{self.name} defends!")
         logger.debug(f"  -> Defense Roll: {die_roll} (d20) + {self.aptitude} (Apt) + {boon_roll} (Boon) - {banes} (Banes) = {total}")
         logger.debug(f"  -> vs DT {attacker_dt}: {outcome.value}")
         return outcome

    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp < 0: self.hp = 0
        logger.debug(f"{self.name} takes {amount} damage. HP: {self.hp}")

    def is_alive(self) -> bool:
        return self.hp > 0
