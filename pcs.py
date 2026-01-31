from typing import Any, Optional, Tuple
import logging
from mechanics import resolve_roll, Outcome, Combatant
from strategies import lowest_dt_strategy
from constants import DEFAULT_PC_HP, DEFAULT_APTITUDE, CRITICAL_DAMAGE, MIN_DAMAGE

logger = logging.getLogger(__name__)

class PC:
    """
    Represents a Player Character.

    Attributes:
        name (str): The name of the PC.
        hp (int): Current Hit Points.
        max_hp (int): Maximum Hit Points.
        aptitude (int): Base bonus added to rolls (default 5).
        expertise_attack (bool): If True, grants 2d20kh on Attack rolls.
        expertise_defense (bool): If True, grants 2d20kh on Defense rolls.
        targeting_strategy (callable): Function to select a target from a list of enemies.
    """
    def __init__(
        self, 
        name: str, 
        expertise_attack: bool = False, 
        expertise_defense: bool = False, 
        targeting_strategy: Any = lowest_dt_strategy
    ):
        """Initializes a PC with health, aptitude, and expertise settings.

        Args:
            name: The display name of the character.
            expertise_attack: If True, grants advantage on attack rolls.
            expertise_defense: If True, grants advantage on defense rolls.
            targeting_strategy: Function used to select targets.
        """
        self.name = name
        self.hp = DEFAULT_PC_HP
        self.max_hp = DEFAULT_PC_HP
        self.aptitude = DEFAULT_APTITUDE
        self.expertise_attack = expertise_attack
        self.expertise_defense = expertise_defense
        self.targeting_strategy = targeting_strategy

    def make_attack(self, target: Any, friction_banes: int) -> tuple[int, Outcome]:
        """
        PC makes an attack roll against a target.

        Args:
            target (Any): The enemy entity being attacked. Must have a 'dt' attribute.
            friction_banes (int): Number of banes accumulated due to friction/momentum.

        Returns:
            tuple[int, Outcome]: A tuple containing the damage dealt (int) and the Outcome enum.
        """
        logger.debug(f"{self.name} attacks {target.name}!")
        
        # Determine Bane Stacks
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
            damage = CRITICAL_DAMAGE
        elif outcome in [Outcome.CLEAN_SUCCESS, Outcome.TRIUMPH]:
             damage = max(MIN_DAMAGE, damage)
        
        return damage, outcome

    def defend_attack(self, attacker: Any, friction_boons: int = 0) -> Outcome:
         """
         PC rolls to defend against an incoming attack.

         Args:
             attacker (Any): The entity attacking the PC. Must have a 'dt' attribute.
             friction_boons (int): Number of boons accumulated due to friction (when NPCs have momentum).

         Returns:
             Outcome: The result of the defense roll.
         """
         attacker_dt = getattr(attacker, 'dt', 12)
         
         bane_stacks = 0
         
         if getattr(attacker, 'expertise_attack', False):
             bane_stacks += 1
             logger.debug(f"  -> Added Bane for Attacker Attack Expertise (Total Banes: {bane_stacks})")
         
         # Friction is applied as boons when defending (NPCs have momentum)
         boon_stacks = 1 + friction_boons  # Base 1 boon + friction boons
             
         # Resolve Defense Roll
         total, nat20, outcome, die_roll, boon_roll, bane_roll = resolve_roll(
             expertise=self.expertise_defense, 
             aptitude=self.aptitude, 
             bane_stacks=bane_stacks, 
             dt=attacker_dt,
             boon_stacks=boon_stacks
         )
         
         logger.debug(f"{self.name} defends against {attacker.name}!")
         logger.debug(f"  -> Defense Roll: {die_roll} (d20) + {self.aptitude} (Apt) + {boon_roll} (Boon, stacks={boon_stacks}) - {bane_roll} (Bane) = {total}")
         logger.debug(f"  -> vs DT {attacker_dt}: {outcome.value}")
         return outcome

    def take_damage(self, amount: int):
        """
        Apply damage to the PC.

        Args:
            amount (int): Amount of damage to subtract from HP.
        """
        self.hp -= amount
        if self.hp < 0: self.hp = 0
        logger.debug(f"{self.name} takes {amount} damage. HP: {self.hp}")

    def is_alive(self) -> bool:
        """
        Check if the PC is alive.

        Returns:
            bool: True if HP > 0, False otherwise.
        """
        return self.hp > 0

