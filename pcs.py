from mechanics import resolve_roll, Outcome
import logging
from typing import Any, Optional
from strategies import lowest_dt_strategy

logger = logging.getLogger(__name__)

class PC:
    def __init__(self, name: str, expertise_attack: bool = False, expertise_defense: bool = False, targeting_strategy=lowest_dt_strategy):
        self.name = name
        self.hp = 4
        self.max_hp = 4
        self.aptitude = 5
        self.expertise_attack = expertise_attack
        self.expertise_defense = expertise_defense
        self.dt = 12 # Default DT
        self.targeting_strategy = targeting_strategy

    def make_attack(self, target: Any, friction_banes: int) -> tuple[int, Outcome]:
        """
        PC attacks an NPC.
        Rolls Attack (Aptitude) vs Target DT.
        Banes = Friction Banes + Target Defense Expertise (1 stack if expert).
        """
        logger.debug(f"{self.name} attacks {target.name}!")
        
        # Determine Bane Stacks
        # 1 from friction? (passed in)
        # 1 from NPC defense expertise?
        
        bane_stacks = friction_banes
        if getattr(target, 'expertise_defense', False):
             bane_stacks += 1
             logger.debug(f"  -> Added Bane for Target Defense Expertise (Total Banes: {bane_stacks})")
        
        # Roll Attack
        total, nat20, outcome, die_roll, boon_roll, bane_roll = resolve_roll(
            expertise=self.expertise_attack, 
            aptitude=self.aptitude, 
            bane_stacks=bane_stacks, 
            dt=target.dt
        )
        
        logger.debug(f"  -> Attack Roll: {die_roll} (d20) + {self.aptitude} (Apt) + {boon_roll} (Boon) - {bane_roll} (Bane) = {total}")
        logger.debug(f"  -> vs DT {target.dt}: {outcome.value}")
        
        damage = 0
        if outcome == Outcome.TRIUMPH:
            damage = 2
        elif outcome == Outcome.CLEAN_SUCCESS:
             pass # Does this mean 1? The original code had pass?? 
             # Looking at original goodies.py:
             # elif outcome == Outcome.CLEAN_SUCCESS:
             #      pass
             #
             # if outcome in [Outcome.CLEAN_SUCCESS, Outcome.TRIUMPH]:
             #      damage = max(1, damage)
             # Thus Clean Success is 1. Triumph is 2.
             
        if outcome in [Outcome.CLEAN_SUCCESS, Outcome.TRIUMPH]:
             damage = max(1, damage)
        
        return damage, outcome

    def make_defense(self, attacker: Any, friction_banes: int) -> Outcome:
         """
         PC defends against an NPC attack.
         Rolls Defense (Aptitude) vs Attacker DT (or standardized DT?).
         The prompt say: "PC's expertise (attack or defense) determines whether the D20 roll is d20 or 2d20kh"
         "NPC's expertise (attack or defense) determines whether a bane is added to the PC's roll."
         
         So PC rolls Defense.
         Expertise: self.expertise_defense
         DT: Attacker DT? (Let's assume standard logic of rolling vs Difficulty)
         Banes: Friction Banes + Attacker Attack Expertise.
         """
         attacker_dt = getattr(attacker, 'dt', 12)
         
         bane_stacks = friction_banes # Friction applies to the actor?
         # Wait. If NPC is attacking (Actor), does Friction apply to THEM?
         # "friction_banes" in engine usually tracks how long the "Momentum Run" is.
         # If NPC is acting, and momentum is NPC, friction applies to NPC actions.
         # Since PC is rolling defense AS the resolution of NPC action, the friction banes likely apply here to make it harder for PC to defend?
         # Or does it make it harder for NPC to hit?
         # If Friction = "Things getting messy/tired", usually applies to the Actor.
         # If NPC is Actor -> They are "attacking".
         # Taking a bane on PC defense roll makes it harder for PC to defend -> Easier for NPC to hit.
         # So Friction Banes should be ADDED to PC Defense roll (making it lower, causing failure).
         
         if getattr(attacker, 'expertise_attack', False):
             bane_stacks += 1
             logger.debug(f"  -> Added Bane for Attacker Attack Expertise (Total Banes: {bane_stacks})")
             
         # Resolve Defense Roll
         total, nat20, outcome, die_roll, boon_roll, bane_roll = resolve_roll(
             expertise=self.expertise_defense, 
             aptitude=self.aptitude, 
             bane_stacks=bane_stacks, 
             dt=attacker_dt
         )
         
         logger.debug(f"{self.name} defends against {attacker.name}!")
         logger.debug(f"  -> Defense Roll: {die_roll} (d20) + {self.aptitude} (Apt) + {boon_roll} (Boon) - {bane_roll} (Bane) = {total}")
         logger.debug(f"  -> vs DT {attacker_dt}: {outcome.value}")
         return outcome

    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp < 0: self.hp = 0
        logger.debug(f"{self.name} takes {amount} damage. HP: {self.hp}")

    def is_alive(self) -> bool:
        return self.hp > 0
