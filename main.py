import random
from goodies import Goodies
from baddies import Baddies
from mechanics import Outcome

# Constants
NUM_SIMULATIONS = 1000

def get_living_members(team):
    return [m for m in team if m.is_alive()]

def select_target(attacker, enemy_team):
    living_enemies = get_living_members(enemy_team)
    if not living_enemies:
        return None
    
    # Player Strategy: Attack lowest DT
    if isinstance(attacker, Goodies):
        # Sort by DT, then random index for tie breaking (stable sort)
        living_enemies.sort(key=lambda x: x.dt)
        return living_enemies[0]
    
    # Enemy Strategy: Random target
    return random.choice(living_enemies)

def select_actor(team, run_actors, is_goodies_team):
    """
    Selects the next character to act based on priority:
    1. Not acted in this run.
    2. Best suited (Attack expert).
    3. Anyone else.
    """
    living = get_living_members(team)
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

def run_battle(battle_id, debug_print=False):
    # Initialize Teams
    # PCs
    # PC 1: Expert Atk & Def
    pc1 = Goodies("PC 1 (Exp Atk/Def)", expertise_attack=True, expertise_defense=True)
    # PC 2: Expert Def
    pc2 = Goodies("PC 2 (Exp Def)", expertise_attack=False, expertise_defense=True)
    # PC 3: Expert Atk
    pc3 = Goodies("PC 3 (Exp Atk)", expertise_attack=True, expertise_defense=False)
    # PC 4-5: Baseline
    pc4 = Goodies("PC 4", expertise_attack=False, expertise_defense=False)
    pc5 = Goodies("PC 5", expertise_attack=False, expertise_defense=False)
    goodies_team = [pc1, pc2, pc3, pc4, pc5]

    # Enemies
    # 6 Minions: DT 12, HP 1
    minions = [Baddies(f"Minion {i+1}", hp=1, dt=12) for i in range(6)]
    # 2 Elites: DT 15, HP 2
    # Elite 1: Exp Atk
    elite1 = Baddies("Elite 1 (Exp Atk)", hp=2, dt=15, expertise_attack=True)
    # Elite 2: Exp Def
    elite2 = Baddies("Elite 2 (Exp Def)", hp=2, dt=15, expertise_defense=True)
    # Boss: DT 18, HP 4, Exp Atk & Def
    boss = Baddies("Boss", hp=4, dt=18, expertise_attack=True, expertise_defense=True)
    
    baddies_team = minions + [elite1, elite2, boss]

    # State
    current_momentum = "goodies" # Starts with players
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
        if not get_living_members(goodies_team):
            if debug_print: print("Enemies Win!")
            break
        if not get_living_members(baddies_team):
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
        actor = select_actor(active_team, run_actors, current_momentum == "goodies")
        target = select_target(actor, passive_team)
        
        if not target:
            break # Should be caught by win check, but safety
            
        # Friction Logic
        # "Friction only begins after every living member ... has acted once"
        # "Once friction begins, each additional action adds +1 Bane"
        
        # Check if we should Activate Friction (if not active)
        # Condition: Have all currently living members acted?
        # Note checks BEFORE adding current actor to set?
        # Prompt: "after every living member ... has acted once".
        # So loop runs: Act 1..N (size). No friction.
        # Next action (N+1): Friction starts? 
        # "Once friction begins..."
        
        living_active = get_living_members(active_team)
        # Check if set covers all living members
        # We check this at the START of the turn selection? 
        # Actually logic is: Once set is full, Friction Active = True. 
        # Then Reset set? No "cumulative".
        # Ah, "Momentum Run ... No friction initially ... Banes reset when Momentum shifts."
        # So we keep adding to run_actors.
        
        # Calculate Banes
        banes = 0
        if friction_active:
            friction_banes += 1
            banes = friction_banes
        
        # Perform Action (Attack)
        if debug_print: print(f"Turn {turn_count}: {actor.name} (Banes: {banes}) attacks {target.name}")
        
        # Attack Roll
        atk_dmg, atk_outcome = actor.make_attack(target=target, banes=banes)
        
        # Defense logic (Target Defends)
        # Target rolls defense vs Attacker's DT? Or Standard?
        # Prompt: "Attacker Rolls... Outcome Bands". 
        # "Catastrophe on defense".
        # Let's say Defense Roll is vs Attacker's DT ??? Or Fixed?
        # Given "Compare total to target's DT", Attack is vs Target DT.
        # Defense Roll needs a DT. Let's use 12 for everyone as a baseline diff?
        # Or better: Defense DC = Attacker's Attack Roll result? (Opposed).
        # Opposed roll is standard for qualitative tests.
        # Let's use Attacker's Total Roll as DT for Defense?
        # Actually, "Target's Difficulty Threshold (DT)".
        # Enemies have DT. PCs have DT?
        # Let's assume PCs have DT 12 (standard) if not specified.
        # So Attack vs Target DT.
        # Defense vs Attacker DT? (Fairness).
        # Let's try: Defense vs 12 (Baseline).
        # Or better yet, maybe Defense doesn't roll unless needed?
        # "Defender steals momentum ... on Triumph or Clean Success".
        # So Defender ALWAYS rolls.
        
        # Check PC DT. Minions 12. Elites 15. Boss 18.
        # Goodies? Let's give them DT 12 + maybe Aptitude? No, Aptitude is for rolling.
        # Let's stick with DT 12 for Goodies validation.
        # If Attacker is Goodie: Attack vs Target (12/15/18).
        # If Defender is Baddie: Defend vs ? (Goodie DT = 12?)
        
        defender_dt = 12
        if isinstance(actor, Baddies):
             defender_dt = actor.dt
        
        # Wait, if Goodie is Attacking, Goodie uses Target (Baddie) DT.
        # Baddie (Defender) uses Goodie (Attacker) DT?
        
        attacker_dt = 12
        if isinstance(actor, Baddies):
            attacker_dt = actor.dt
        
        # Actually, if I am defending against an Attack, the difficulty should correspond to the Attack?
        # But Prompt says "Compare total to target's Difficulty Threshold".
        # This is for the primary roll.
        # Let's just use 12 for "Generic Challenge" for Defense rolls to keep it simple and consistent.
        
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
        # "after every living member ... has acted once"
        if not friction_active:
             # Check if all living members are in run_actors
             all_acted = True
             for m in living_active:
                 if m not in run_actors:
                     all_acted = False
                     break
             if all_acted:
                 friction_active = True
                 # "active after every living acted once".
                 # Does the penalty start NOW or next turn?
                 # "Once friction begins, each additional action adds..."
                 # So next turn.
        
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
    # Usually run ends when battle ends. Or maybe not "Momentum Run" if interrupted by win.
    # Prompt: "Track every Momentum Run".
    # Assuming partial run at end counts? Yes.
    if run_length > 0:
        if current_momentum == "goodies":
            goodies_run_lengths.append(run_length)
        else:
            baddies_run_lengths.append(run_length)
            
    return goodies_run_lengths, baddies_run_lengths

def simulation_loop():
    print(f"Starting {NUM_SIMULATIONS} Simulations...")
    
    total_goodies_runs = []
    total_baddies_runs = []
    
    for i in range(NUM_SIMULATIONS):
        # Print first battle for validation
        debug = (i == 0)
        g_runs, b_runs = run_battle(i+1, debug_print=debug)
        total_goodies_runs.extend(g_runs)
        total_baddies_runs.extend(b_runs)
        
    avg_goodies = sum(total_goodies_runs) / len(total_goodies_runs) if total_goodies_runs else 0
    avg_baddies = sum(total_baddies_runs) / len(total_baddies_runs) if total_baddies_runs else 0
    
    print("\n=== Simulation Results ===")
    print(f"Average run length for players: {avg_goodies:.2f}")
    print(f"Average run length for enemies: {avg_baddies:.2f}")

def main():
    simulation_loop()

if __name__ == "__main__":
    main()

