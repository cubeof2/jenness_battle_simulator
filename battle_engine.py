import random
import logging
from typing import List, Set, Any, Tuple
from pcs import PC
from npcs import NPC
from mechanics import Outcome

logger = logging.getLogger(__name__)

def get_living_members(team: List[Any]) -> List[Any]:
    """Returns a list of members in the team that are currently alive."""
    return [m for m in team if m.is_alive()]

def select_target(attacker: Any, enemy_team: List[Any]) -> Any:
    """
    Selects a target from the enemy team using the attacker's strategy.
    
    Args:
        attacker (Any): The entity initiating the action.
        enemy_team (List[Any]): List of potential targets.
        
    Returns:
        Any: The selected target, or None if no valid targets exist.
    """
    # Use the attacker's strategy if available
    if hasattr(attacker, 'targeting_strategy'):
        return attacker.targeting_strategy(attacker, enemy_team)
    
    # Fallback to random if no strategy defined
    living_enemies = get_living_members(team=enemy_team)
    if not living_enemies:
        return None
    return random.choice(living_enemies)

def select_actor(team: List[Any], run_actors: Set[Any]) -> Any:
    """
    Selects the next character to act from the team.
    
    Priority:
    1. Members who have not yet acted in this run.
    2. Members with Attack Expertise.
    3. Any other member.
    
    Args:
        team (List[Any]): The team currently holding momentum.
        run_actors (Set[Any]): Set of actors who have already acted in the current run.
        
    Returns:
        Any: The selected actor.
    """
    living = get_living_members(team=team)
    not_acted = [m for m in living if m not in run_actors]
    
    candidates = not_acted if not_acted else living
    
    # Filter for Attack Experts if possible
    experts = [c for c in candidates if c.expertise_attack]
    others = [c for c in candidates if not c.expertise_attack]
    
    # Prefer experts for action selection (Attacking)
    if experts:
        return experts[0] # Pick first expert
    if others:
        return others[0]
    return candidates[0] # Fallback, shouldn't happen if list not empty

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
    pcs_team = []
    for g_conf in scenario_config["pcs"]:
        pcs_team.append(PC(
            name=g_conf["name"], 
            expertise_attack=g_conf.get("exp_atk", False), 
            expertise_defense=g_conf.get("exp_def", False)
        ))
        
    npcs_team = []
    for b_conf in scenario_config["npcs"]:
        npcs_team.append(NPC(
            name=b_conf["name"], 
            hp=b_conf["hp"], 
            dt=b_conf["dt"], 
            expertise_attack=b_conf.get("exp_atk", False), 
            expertise_defense=b_conf.get("exp_def", False)
        ))

    # State
    current_momentum = scenario_config.get("starting_momentum", "pcs")
    run_actors = set() # Track who acted in current run
    run_length = 0
    friction_banes = 0
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
        
        # Calculate Friction Banes for this Turn
        banes = 0
        if friction_active:
            friction_banes += 1
            banes = friction_banes
        
        logger.debug(f"Turn {turn_count}: {actor.name} (Banes: {banes}) acts against {target.name}")
        
        # --- EXECUTE ACTION ---
        outcome = Outcome.FAILURE # Default
        momentum_shift = False # Default

        if isinstance(actor, PC):
            # PC Attacking NPC
            damage, outcome = actor.make_attack(target=target, friction_banes=banes)
            
            if damage > 0:
                target.take_damage(amount=damage)
            
            # PC Success (Keep Momentum) = Clean Success or Triumph
            if outcome in [Outcome.CLEAN_SUCCESS, Outcome.TRIUMPH]:
                momentum_shift = False
                logger.debug("PC Attack Successful! Momentum Retained.")
            else:
                momentum_shift = True
                logger.debug("PC Attack Failed! Momentum Lost.")

        elif isinstance(actor, NPC):
            # NPC Attacking PC -> PC Defends
            # Note: banes passed here are friction banes. PC.defend_attack will add NPC attack expertise as bane too.
            outcome = target.defend_attack(attacker=actor, friction_banes=banes)
            
            # Defense Success (PC Avoids) = Clean Success or Triumph
            # Defense Failure (PC Hit) = Failure, Setback, Catastrophe
            
            damage_to_pc = 0
            if outcome == Outcome.CATASTROPHE:
                damage_to_pc = 2
                logger.debug("PC Defense Catastrophe! Takes 2 Damage.")
            elif outcome in [Outcome.FAILURE, Outcome.SETBACK]:
                damage_to_pc = 1
                logger.debug(f"PC Defense {outcome.value}! Takes 1 Damage.")
            
            if damage_to_pc > 0:
                target.take_damage(amount=damage_to_pc)
                
            # If PC Defended Successfully (Clean/Triumph), they STEAL momentum.
            # If PC Failed (NPC Hit), NPC KEEPS momentum.
            
            if outcome in [Outcome.CLEAN_SUCCESS, Outcome.TRIUMPH]:
                momentum_shift = True
                logger.debug("PC Defended Successfully! Momentum Stolen.")
            else:
                momentum_shift = False
                logger.debug("PC Defense Failed/Setback. NPC Keeps Momentum.")

        # Update Run State (Action successfully taken)
        run_actors.add(actor)
        run_length += 1
        
        # Check friction trigger for NEXT turn
        if not friction_active:
             # Check if all living members are in run_actors
             all_acted = True
             for m in living_active:
                 if m not in run_actors:
                     all_acted = False
                     break
             if all_acted:
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
            friction_banes = 0
            friction_active = False
            
    # End of Battle - Record last run
    if run_length > 0:
        if current_momentum == "pcs":
            pcs_run_lengths.append(run_length)
        else:
            npcs_run_lengths.append(run_length)
            
    winner = "pcs" if get_living_members(pcs_team) else "npcs"
    return pcs_run_lengths, npcs_run_lengths, winner


