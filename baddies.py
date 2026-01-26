from mechanics import resolve_roll, Outcome

class Baddies:
    def __init__(self, name, hp, dt, expertise_attack=False, expertise_defense=False):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.dt = dt
        self.expertise_attack = expertise_attack
        self.expertise_defense = expertise_defense
        self.aptitude = 0 # Enemies have 0 aptitude bonus? Prompt says "Combatants Player Characters ... Aptitude bonus: +5". Enemies: No mention. Assume 0.

    def make_attack(self, target, banes, debug=True):
        if debug:
            print(f"{self.name} attacks {target.name}!")
        
        total, nat20, outcome, die_roll, boon_roll = resolve_roll(self.expertise_attack, self.aptitude, banes, target.dt)
        
        if debug:
            print(f"  -> Attack Roll: {die_roll} (d20) + {self.aptitude} (Apt) + {boon_roll} (Boon) - {banes} (Banes) = {total}")
            print(f"  -> vs DT {target.dt}: {outcome.value}")

        damage = 0
        if outcome == Outcome.TRIUMPH:
            damage = 2
        elif outcome == Outcome.CLEAN_SUCCESS:
             damage = 1
        
        return damage, outcome

    def make_defense(self, attacker_dt, banes, debug=True):
         total, nat20, outcome, die_roll, boon_roll = resolve_roll(self.expertise_defense, self.aptitude, banes, attacker_dt)
         if debug:
             print(f"{self.name} defends!")
             print(f"  -> Defense Roll: {die_roll} (d20) + {self.aptitude} (Apt) + {boon_roll} (Boon) - {banes} (Banes) = {total}")
             print(f"  -> vs DT {attacker_dt}: {outcome.value}")
         return outcome

    def take_damage(self, amount, debug=True):
        self.hp -= amount
        if self.hp < 0: self.hp = 0
        if debug:
            print(f"{self.name} takes {amount} damage. HP: {self.hp}")

    def is_alive(self):
        return self.hp > 0
