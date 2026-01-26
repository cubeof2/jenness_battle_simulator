from mechanics import resolve_roll, Outcome

class Goodies:
    def __init__(self, name, expertise_attack=False, expertise_defense=False):
        self.name = name
        self.hp = 4
        self.max_hp = 4
        self.aptitude = 5
        self.expertise_attack = expertise_attack
        self.expertise_defense = expertise_defense
        self.dt = 10 # Default DT for players? Not specified, assuming average or handled by enemies attacking them.
        # Wait, enemies attack players, so players need a DT. 
        # Request doesn't specify Player DT, only Enemy DT (12, 15, 18).
        # "Target's Difficulty Threshold". 
        # Lets assume Player DT is ... 12? Or maybe they defend using the roll?
        # Re-reading: "PC 2: Expert in defense only -> 2d20 kh1 on defense"
        # "Catastrophe on defense: defender takes 2 HP"
        # This implies Players ROLL for defense. 
        # "Dice & Resolution Core Roll: Roll = ... Compare total to target's DT"
        # If players defend, they are rolling against Enemy's Attack DT? Or Enemy rolls against Player DT?
        # The prompt says: "PCs ... Expert in defense only". "Enemies... One expert in defense".
        # This implies active defense rolls.
        # However, usually D20 combat is Attacker Rolls vs Static DT.
        # Or Opposed Rolls.
        # Prompt: "Combat Rules: Momentum ... One side has Momentum ... chooses eligible character to act."
        # If it's your turn (Momentum), you Act. Action is usually Attack.
        # If proper turn-based, only current actor rolls.
        # If I attack Enemy, I roll vs Enemy DT.
        # If Enemy attacks Me, Enemy rolls vs My DT?
        # But PC 2 is "Expert in defense". When do they roll defense?
        # Maybe Defense is a reaction? Or maybe pure "Defense" action to recover/buff?
        # BUT: "Catastrophe on defense: defender takes 2 HP".
        # If I roll Defense, it implies I am being attacked.
        # Momentum Rules: "Defender steals Momentum only on Triumph or Clean Success".
        # This implies the Defender DOES roll.
        # So it's likely: Attacker Rolls vs Defender Rolls? Or Attacker Rolls vs Static DT, and Defender Rolls vs Static DT (to soak)?
        # Actually "Compare total to target's Difficulty Threshold (DT)". This implies Attacker Rolls vs Static DT.
        # Then what is "Expert in defense"?
        # Maybe "Defense" is an action you can take on your turn?
        # OR: When attacked, you roll to defend?
        # "Dice & Resolution ... Compare total to target's Difficulty Threshold (DT)" -> Describes the ROLL.
        # "Outcome Bands ... Catastrophe on defense: defender takes 2 HP".
        # This strongly implies Defense is a ROLL.
        # Let's assume: When Attacked, you Roll Defense vs some DT (maybe Attacker's DT or standard).
        # OR: Attacker rolls Attack, Defender rolls Defense. Compare?
        # Let's look at "Momentum": "Defender steals Momentum ... on Triumph or Clean Success".
        # This confirms Defender ROLLS.
        # Let's assume standard 'Player Facing' rolls? No, Enemies also have expertise.
        # Let's assume OPPOSED ROLLS or both roll vs DT.
        # Given "Compare total to target's DT", let's assume:
        # Attacker Rolls vs Target DT.
        # Defender Rolls vs Attacker DT (to dodge)?
        # Let's simplify: 
        # Attack Action: Attacker Rolls vs Target DT. 
        # Defend Reaction: When attacked, Defender Rolls vs Attacker's ("Target") DT/Attack Result?
        # Let's stick to the prompt most literal interpretation:
        # "Catastrophe on defense" -> Defense is a roll.
        # "PC 2 Expert in defense".
        # Let's assume when a character is the TARGET of an attack, they make a Defense Roll?
        # Or maybe Defense is an action to 'Recover/Buff'? (Unlikely given "Defender steals momentum").
        # Ok, simplest interpretation supporting all points:
        # When X attacks Y:
        # X Rolls Attack vs Y's DT. (To hit)
        # Y Rolls Defense vs X's DT? or a fixed DT? (To avoid/mitigate)
        # If "Result vs Target DT" is the core mechanic.
        # Let's assume: Attacker Rolls. Outcome determines hit. 
        # But then how does Defender get "Clean Success" to steal momentum?
        # Re-read: "Defender steals Momentum only on: Triumph or Clean Success".
        # Implies Defender IS rolling. 
        # If the Attacker is rolling against the Defender, the Defender is passive.
        # UNLESS "Defender" here refers to the Side resisting the current Momentum turn?
        # No, "Defender steals Momentum...".
        # It's possible ONLY the side with MOMENTUM makes rolls (Players or Enemies).
        # "The side with Momentum chooses one eligible character to act."
        # If I have Momentum, I attack. I roll.
        # If I fail (Setback/Failure), Momentum shifts.
        # Does the ENEMY roll to defend?
        # "Defense" expertise exists.
        # Let's assume Active Opposition: Both sides roll?
        # Or maybe: 
        # 1. Attacker Acts (Rolls Attack).
        # 2. If Attack Fails, Momentum Shift. 
        # 3. If Attack Succeeds, Damage? 
        # Where does Defense come in?
        # Maybe "Defense" is the Roll you make when you DON'T have momentum?
        # No, "Momentum starts with players. The side with Momentum chooses one character to act."
        # So the other side does nothing?
        # Then how do they use "Defense Expertise"?
        # Maybe Defense is a specific Action you can take when you HAVE momentum? 
        # But "Catastrophe on defense: defender takes 2 HP" sounds like being hit.
        # Let's assume:
        # The Acting Character Rolls (Attack or other action).
        # The TARGET opposes? 
        # Actually, maybe the simplest:
        # Attack Roll vs Target DT.
        # If Outcome is Failure/Catastrophe -> Defender "wins" interaction? 
        # If Attacker fails, Defender "Clean Success"? No that maps Outcomes to Attacker Roll.
        # Let's assume the "Defender" means the character being attacked, and they ROLL to defend.
        # So: Attacker Rolls Attack vs Target DT. Defender Rolls Defense vs Attacker DT (or static).
        # If Attacker Wins -> Hit.
        # If Defender Wins -> Miss.
        # That seems complex and maybe overkill.
        # Alternative: "Defense" is just ability to resist.
        # But "Expertise in Defense" = "2d20 kh1". That is a ROLL modifier.
        # So Defense MUST be a roll.
        # Does every attack involve 2 rolls? Attack vs Defense?
        # Most likely.
        # Let's Implement: Attack Roll vs Target DT. Defense Roll vs Attacker DT.
        # Compare outcomes? 
        # Or maybe Defense Roll is just to see if they Steal Momentum?
        # Let's go with:
        # Attacker rolls vs Target DT. Outcome determines damage/momentum-keep.
        # Defender rolls vs Attacker DT. Outcome determines negate/momentum-steal?
        # Let's assume: 
        # Attacker acts. Rolls Attack. 
        # Defender reacts. Rolls Defense.
        # Damage happens if Attack succeeds AND Defense fails?
        # Let's try to infer from "Catastrophe on defense: defender takes 2 HP".
        # If I roll Defense and get Catastrophe, I take damage.
        # This implies Defense is a risky roll you make to stop an attack.
        # Plan:
        # Engagement:
        # 1. Attacker Rolls Attack vs Target DT.
        # 2. Defender Rolls Defense vs Attacker DT (implied 10 or 12 for PCs? Prompt doesn't say PC DT).
        # Let's set PC DT = 12 (same as Minions) for now as default.
        # Outcomes:
        # If Attacker Succeeded (Clean/Triumph): Damage. Retain Momentum.
        # If Defender Succeeded (Clean/Triumph): Steal Momentum.
        # What if both succeed? Momentum check priority? 
        # "Defender steals... ONLY on Triumph or Clean Success".
        # "Acting side retains... ONLY on Triumph or Clean Success".
        # If Attacker Clean Success (Hit) AND Defender Clean Success (Dodge/Parry) -> ?
        # Usually Defender wins ties or status quo changes.
        # Let's stick to the Prompt's "Damage Rules":
        # "Normal hit: 1 HP". (Implies success on attack?)
        # "Triumph on attack: 2 HP".
        # "Catastrophe on defense: defender takes 2 HP".
        # This suggests outcomes are independent events?
        # This is getting complicated. Let's make a decision:
        # ATTACKER ROLLS.
        # If Attack is Setback/Failure/Catastrophe -> Miss. Momentum Shifts.
        # If Attack is Clean Success/Triumph -> Hit. Retain Momentum.
        # DEFENDER ROLLS simultaneously?
        # If Defender Clean Success/Triumph -> Steal Momentum. (Overrides Attacker Retain?)
        # If Defender Catastrophe -> Take Extra Damage? (Or Take Damage even if Attacker missed?)
        # Let's implement independent rolls.
        # Attacker tries to Hit. Defender tries to Defend.
        # If Attacker Hits -> 1 HP. (Triumph -> 2 HP).
        # If Defender Defends (Clean/Triumph) -> Steal Momentum.
        # If Defender Catastrophe -> Take 2 HP (self-inflicted or opportunity).
        # This seems to cover all rules.
        
        self.dt = 12 # Default DT for now

    def make_attack(self, target, banes):
        print(f"{self.name} attacks {target.name}!")
        # Roll Attack
        total, nat20, outcome = resolve_roll(self.expertise_attack, self.aptitude, banes, target.dt)
        
        damage = 0
        if outcome == Outcome.TRIUMPH:
            damage = 2
        elif outcome == Outcome.CLEAN_SUCCESS: # Check "Normal hit" triggers? "Clean Success: total >= DT+3". 
             # Wait, "Normal hit: 1 HP". Does Setback hit?
             # "Setback: total within DT +/- 2".
             # "Failure: total < DT - 2".
             # Usually Setback is "Success with cost" or "Failure with partial".
             # Let's assume: Clean Success = Hit. Triumph = Crit Hit. 
             # Setback = ? (Maybe Hit but Momentum shifts? Or Miss but Momentum stays?)
             # "Retaining Momentum ... ONLY on Triumph or Clean Success". 
             # So Setback = Loss of Momentum. 
             # Does Setback deal damage?
             # "Normal hit: 1 HP".
             # If Setback is a "Miss", it deals 0. 
             # Let's assume Setback is a MISS (or ineffective hit) for damage purposes, given the specific categories. 
             # OR Setback is a HIT that loses momentum.
             # Prompt: "Damage Rules... Normal hit: 1 HP". Doesn't map Outcome to "Normal hit".
             # Implied: Clean Success = Normal Hit. Triumph = Crit.
             # Setback/Failure/Catastrophe = Miss/No Damage.
             pass
        if outcome in [Outcome.CLEAN_SUCCESS, Outcome.TRIUMPH]:
             damage = max(1, damage)
        
        return damage, outcome

    def make_defense(self, attacker_dt, banes):
         # Resolve Defense Roll
         total, nat20, outcome = resolve_roll(self.expertise_defense, self.aptitude, banes, attacker_dt)
         return outcome

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0: self.hp = 0
        print(f"{self.name} takes {amount} damage. HP: {self.hp}")

    def is_alive(self):
        return self.hp > 0
