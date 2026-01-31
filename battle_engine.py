import random
import logging
from typing import List, Set, Tuple, Optional
from pcs import PC
from npcs import NPC
from mechanics import Outcome, Combatant

logger = logging.getLogger(__name__)

def get_living_members(team: List[Combatant]) -> List[Combatant]:
    """Returns a list of members in the team that are currently alive."""
    return [m for m in team if m.is_alive()]

def select_target(attacker: Combatant, enemy_team: List[Combatant]) -> Optional[Combatant]:
    """
    Selects a target from the enemy team using the attacker's strategy.
    
    Args:
        attacker: The entity initiating the action.
        enemy_team: List of potential targets.
        
    Returns:
        The selected target, or None if no valid targets exist.
    """
    # Use the attacker's strategy if available
    if hasattr(attacker, 'targeting_strategy'):
        return attacker.targeting_strategy(attacker, enemy_team)
    
    # Fallback to random if no strategy defined
    living_enemies = get_living_members(team=enemy_team)
    if not living_enemies:
        return None
    return random.choice(living_enemies)

def select_actor(team: List[Combatant], run_actors: Set[Combatant]) -> Combatant:
    """Selects the next character to act from the team based on expertise and turn state."""
    living = get_living_members(team=team)
    not_acted = [m for m in living if m not in run_actors]
    
    candidates = not_acted if not_acted else living
    
    # Filter for Attack Experts if possible
    experts = [c for c in candidates if getattr(c, 'expertise_attack', False)]
    others = [c for c in candidates if not getattr(c, 'expertise_attack', False)]
    
    # Prefer experts for action selection (Attacking)
    if experts:
        return experts[0]
    return others[0] if others else candidates[0]

def run_battle(battle_id: int, scenario_config: dict) -> Tuple[List[int], List[int], str]:
    """
    Executes a single battle simulation.
    
    Args:
        battle_id (int): Identifier for this battle.
        scenario_config (dict): Configuration dictionary defining teams and settings.
        
    Returns:
        Tuple[List[int], List[int], str]: 
            - List of PC run lengths (consecutive successful actions).
            - List of NPC run lengths.
            - Winner string ("pcs" or "npcs").
    """
    # Initialize Teams from Scenario Config
    pcs_team = [PC(**p) for p in scenario_config.get("pcs", [])]
    npcs_team = [NPC(**n) for n in scenario_config.get("npcs", [])]

    # State
    current_momentum = scenario_config.get("starting_momentum", "pcs")
    run_actors = set() # Track who acted in current run
    run_length = 0
    friction_stacks = 0  # Renamed: applied as banes or boons depending on momentum
    friction_active = False # Friction starts AFTER everyone acted once

    # Stats Tracking
    pcs_run_lengths = []
    npcs_run_lengths = []
    
    turn_count = 0
    
    logger.debug(f"=== Battle {battle_id} Start ===")

    while True:
        # Check Win
        if not get_living_members(team=pcs_team):
            logger.debug("NPCs Win!")
            break
        if not get_living_members(team=npcs_team):
            logger.debug("PCs Win!")
            break
            
        turn_count += 1
        
        # Identify Active Team and Passive Team
        if current_momentum == "pcs":
            active_team = pcs_team
            passive_team = npcs_team
        else:
            active_team = npcs_team
            passive_team = pcs_team
            
        # Select Actor and Target
        actor = select_actor(team=active_team, run_actors=run_actors)
        target = select_target(attacker=actor, enemy_team=passive_team)
        
        if not target:
            break # Should be caught by win check
            
        # Friction Logic
        living_active = get_living_members(team=active_team)
        
        # Calculate Friction for this Turn
        friction_count = 0
        if friction_active:
            friction_stacks += 1
            friction_count = friction_stacks
        
        logger.debug(f"Turn {turn_count}: {actor.name} (Friction: {friction_count}) acts against {target.name}")
        
        # --- EXECUTE ACTION ---
        momentum_shift = False

        if isinstance(actor, PC):
            from constants import CRITICAL_DAMAGE
            # PC Attacking NPC - PC has momentum, friction applies as banes
            damage, outcome = actor.make_attack(target=target, friction_banes=friction_count)
            
            if damage > 0:
                target.take_damage(amount=damage)
            
            # PC Success (Keep Momentum) = Clean Success or Triumph
            momentum_shift = outcome not in [Outcome.CLEAN_SUCCESS, Outcome.TRIUMPH]
            logger.debug(f"PC Attack {outcome.value}! Momentum {'Lost' if momentum_shift else 'Retained'}.")

        elif isinstance(actor, NPC):
            # NPC Attacking PC -> PC Defends
            # Friction applies as BOONS to PC (NPCs have momentum)
            outcome = target.defend_attack(attacker=actor, friction_boons=friction_count)
            
            damage_to_pc = 0
            if outcome == Outcome.CATASTROPHE:
                damage_to_pc = CRITICAL_DAMAGE
            elif outcome in [Outcome.FAILURE, Outcome.SETBACK]:
                damage_to_pc = 1
            
            if damage_to_pc > 0:
                target.take_damage(amount=damage_to_pc)
                
            # If PC Defended (Clean/Triumph), they STEAL momentum.
            momentum_shift = outcome in [Outcome.CLEAN_SUCCESS, Outcome.TRIUMPH]
            logger.debug(f"PC Defense {outcome.value}! Momentum {'Stolen' if momentum_shift else 'NPC Keeps'}.")

        # Update Run State
        run_actors.add(actor)
        run_length += 1
        
        # Check friction trigger for NEXT turn
        if not friction_active and all(m in run_actors for m in living_active):
            friction_active = True
        
        # Handle Momentum Shift
        if momentum_shift:
            # Record Run Length
            if current_momentum == "pcs":
                pcs_run_lengths.append(run_length)
                current_momentum = "npcs"
                logger.debug("Momentum shifts to NPCs.")
            else:
                npcs_run_lengths.append(run_length)
                current_momentum = "pcs"
                logger.debug("Momentum shifts to PCs.")
            
            # Reset Run State
            run_actors = set()
            run_length = 0
            friction_stacks = 0
            friction_active = False
            
    # End of Battle - Record last run
    if run_length > 0:
        if current_momentum == "pcs":
            pcs_run_lengths.append(run_length)
        else:
            npcs_run_lengths.append(run_length)
            
    winner = "pcs" if get_living_members(pcs_team) else "npcs"
    return pcs_run_lengths, npcs_run_lengths, winner


