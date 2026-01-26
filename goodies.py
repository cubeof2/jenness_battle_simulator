from mechanics import resolve_roll, Outcome
import logging
from typing import Any, List, Optional
from strategies import lowest_dt_strategy

logger = logging.getLogger(__name__)

class Goodies:
    def __init__(self, name: str, expertise_attack: bool = False, expertise_defense: bool = False, targeting_strategy=lowest_dt_strategy):
        self.name = name
        self.hp = 4
        self.max_hp = 4
        self.aptitude = 5
        self.expertise_attack = expertise_attack
        self.expertise_defense = expertise_defense
        self.dt = 12 # Default DT
        self.targeting_strategy = targeting_strategy

    def make_attack(self, target: Any, banes: int) -> tuple[int, Outcome]:
        logger.debug(f"{self.name} attacks {target.name}!")
        
        # Roll Attack
        total, nat20, outcome, die_roll, boon_roll = resolve_roll(self.expertise_attack, self.aptitude, banes, target.dt)
        
        logger.debug(f"  -> Attack Roll: {die_roll} (d20) + {self.aptitude} (Apt) + {boon_roll} (Boon) - {banes} (Banes) = {total}")
        logger.debug(f"  -> vs DT {target.dt}: {outcome.value}")
        
        damage = 0
        if outcome == Outcome.TRIUMPH:
            damage = 2
        elif outcome == Outcome.CLEAN_SUCCESS:
             pass
             
        if outcome in [Outcome.CLEAN_SUCCESS, Outcome.TRIUMPH]:
             damage = max(1, damage)
        
        return damage, outcome

    def make_defense(self, attacker_dt: int, banes: int) -> Outcome:
         # Resolve Defense Roll
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

