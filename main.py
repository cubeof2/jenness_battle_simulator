import random
import time

from goodies import Goodies
from baddies import Baddies

def capture_statistics():
    print("Capturing statistics... (Placeholder)")

def turn_loop(attacker, targets):
    if not attacker.is_alive():
        return

    # Simple AI: attack a random living target
    living_targets = [t for t in targets if t.is_alive()]
    if not living_targets:
        return

    target = random.choice(living_targets)
    attacker.attack(target)

def round_loop(goodies_team, baddies_team):
    print("\n--- New Round ---")
    
    # Goodies turn
    for goodie in goodies_team:
        turn_loop(goodie, baddies_team)

    # Baddies turn
    for baddie in baddies_team:
        turn_loop(baddie, goodies_team)

def battle_loop(goodies_team, baddies_team):
    round_count = 0
    while True:
        # Check win conditions
        if not any(g.is_alive() for g in goodies_team):
            print("Baddies win!")
            break
        if not any(b.is_alive() for b in baddies_team):
            print("Goodies win!")
            break
        
        round_count += 1
        print(f"Round {round_count}")
        round_loop(goodies_team, baddies_team)
        
        # Optional: Sleep for readability if watching live
        # time.sleep(1) 

def simulation_loop():
    print("Starting Simulation...")
    # Setup Teams
    goodies_team = [
        Goodies("Hero", 100, 20),
        Goodies("Sidekick", 80, 15)
    ]
    baddies_team = [
        Baddies("Villain", 120, 18),
        Baddies("Minion", 50, 10)
    ]

    battle_loop(goodies_team, baddies_team)
    capture_statistics()
    print("Simulation Complete.")

def main():
    simulation_loop()

if __name__ == "__main__":
    main()
