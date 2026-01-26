import random
from goodies import Goodies
from baddies import Baddies
from mechanics import Outcome

def get_living_members(team):
    return [m for m in team if m.is_alive()]

def select_target(attacker, enemy_team):
    living_enemies = get_living_members(team=enemy_team)
    if not living_enemies:
        return None
    
    # Player Strategy: Attack lowest DT
    if isinstance(attacker, Goodies):
        # Sort by DT, then random index for tie breaking (stable sort)
        living_enemies.sort(key=lambda x: x.dt)
        return living_enemies[0]
    
    # Enemy Strategy: Random target
    return random.choice(living_enemies)

def select_actor(team, run_actors):
    """
    Selects the next character to act based on priority:
    1. Not acted in this run.
    2. Best suited (Attack expert).
    3. Anyone else.
    """
    living = get_living_members(team=team)
    not_acted = [m for m in living if m not in run_actors]
    
    candidates = not_acted if not_acted else living
    
    # Filter for Attack Experts if possible
    # For Goodies: PC 1 (Atk & Def), PC 3 (Atk only) are experts.
    # For Baddies: One Elite is expert. Boss is expert.
    
    experts = [c for c in candidates if c.expertise_attack]
    others = [c for c in candidates if not c.expertise_attack]
    
    # Prefer experts for attacking
    if experts:
        return experts[0] # Pick first expert
    if others:
        return others[0]
    return candidates[0] # Fallback, shouldn't happen if list not empty

def run_battle(battle_id, scenario_config, debug_print=False):
    # Initialize Teams from Scenario Config
    goodies_team = []
    for g_conf in scenario_config["goodies"]:
        goodies_team.append(Goodies(
            name=g_conf["name"], 
            expertise_attack=g_conf.get("exp_atk", False), 
            expertise_defense=g_conf.get("exp_def", False)
        ))
        
    baddies_team = []
    for b_conf in scenario_config["baddies"]:
        baddies_team.append(Baddies(
            name=b_conf["name"], 
            hp=b_conf["hp"], 
            dt=b_conf["dt"], 
            expertise_attack=b_conf.get("exp_atk", False), 
            expertise_defense=b_conf.get("exp_def", False)
        ))

    # State
    current_momentum = scenario_config.get("starting_momentum", "goodies")
    run_actors = set() # Track who acted in current run
    run_length = 0
    friction_banes = 0
    friction_active = False # Friction starts AFTER everyone acted once

    # Stats Tracking
    goodies_run_lengths = []
    baddies_run_lengths = []
    
    turn_count = 0
    
    if debug_print:
        print(f"=== Battle {battle_id} Start ===")

    while True:
        # Check Win
        if not get_living_members(team=goodies_team):
            if debug_print: print("Enemies Win!")
            break
        if not get_living_members(team=baddies_team):
            if debug_print: print("Players Win!")
            break
            
        turn_count += 1
        
        # Identify Active Team and Passive Team
        if current_momentum == "goodies":
            active_team = goodies_team
            passive_team = baddies_team
        else:
            active_team = baddies_team
            passive_team = goodies_team
            
        # Select Actor
        actor = select_actor(team=active_team, run_actors=run_actors)
        target = select_target(attacker=actor, enemy_team=passive_team)
        
        if not target:
            break # Should be caught by win check, but safety
            
        # Friction Logic
        # "Friction only begins after every living member ... has acted once"
        # "Once friction begins, each additional action adds +1 Bane"
        
        living_active = get_living_members(team=active_team)
        
        # Calculate Banes
        banes = 0
        if friction_active:
            friction_banes += 1
            banes = friction_banes
        
        # Perform Action (Attack)
        if debug_print: print(f"Turn {turn_count}: {actor.name} (Banes: {banes}) attacks {target.name}")
        
        # Attack Roll
        atk_dmg, atk_outcome = actor.make_attack(target=target, banes=banes)
        
        attacker_dt = 12
        if isinstance(actor, Baddies):
            attacker_dt = actor.dt
        
        def_outcome = target.make_defense(attacker_dt=attacker_dt, banes=0) # Defender has no friction banes
        
        # Resolve Damage
        damage_to_target = atk_dmg
        if def_outcome == Outcome.CATASTROPHE:
            if debug_print: print("Defense Catastrophe! +2 Damage")
            damage_to_target += 2
            
        if damage_to_target > 0:
            target.take_damage(amount=damage_to_target)
            
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
        
        # Check Momentum Shift
        # "Acting side retains ... ONLY on Triumph or Clean Success"
        # "Defender steals ... ONLY on Triumph or Clean Success"
        
        attacker_keeps = atk_outcome in [Outcome.TRIUMPH, Outcome.CLEAN_SUCCESS]
        defender_steals = def_outcome in [Outcome.TRIUMPH, Outcome.CLEAN_SUCCESS]
        
        momentum_shift = False
        
        if defender_steals:
            momentum_shift = True
            if debug_print: print("Momentum Stolen by Defender!")
        elif attacker_keeps:
            momentum_shift = False
            if debug_print: print("Momentum Retained by Attacker!")
        else:
            momentum_shift = True
            if debug_print: print("Momentum Lost (Failed to Retain)!")
            
        if momentum_shift:
            # Record Run Length
            if current_momentum == "goodies":
                goodies_run_lengths.append(run_length)
                current_momentum = "baddies"
            else:
                baddies_run_lengths.append(run_length)
                current_momentum = "goodies"
            
            # Reset Run State
            run_actors = set()
            run_length = 0
            friction_banes = 0
            friction_active = False
            if debug_print: print(f"Momentum Shifts to {current_momentum}!")
            
    # End of Battle - Record last run?
    if run_length > 0:
        if current_momentum == "goodies":
            goodies_run_lengths.append(run_length)
        else:
            baddies_run_lengths.append(run_length)
            
    winner = "goodies" if get_living_members(goodies_team) else "baddies"
    return goodies_run_lengths, baddies_run_lengths, winner
