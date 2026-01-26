from battle_engine import run_battle
import statistics
import json
import os

# Constants
NUM_SIMULATIONS = 500
SCENARIO_FILE = "scenarios.json"
SELECTED_SCENARIO_ID = "small_skirmish" # Change this to "small_skirmish" to test

def load_scenarios():
    if not os.path.exists(SCENARIO_FILE):
        print(f"Error: {SCENARIO_FILE} not found.")
        return {}
    
    with open(SCENARIO_FILE, 'r') as f:
        data = json.load(f)
        
    return {s['id']: s for s in data['scenarios']}

def print_detailed_stats(name, data):
    if not data:
        print(f"{name}: No data collected.")
        return
        
    _min = min(data)
    _max = max(data)
    _mean = statistics.mean(data)
    _median = statistics.median(data)
    
    # Calculate IQR
    # Try using statistics.quantiles (Python 3.8+)
    try:
        qs = statistics.quantiles(data, n=4)
        q1 = qs[0]
        q3 = qs[2]
    except AttributeError:
        # Fallback
        sorted_data = sorted(data)
        n = len(sorted_data)
        q1 = sorted_data[int(n * 0.25)]
        q3 = sorted_data[int(n * 0.75)]
        
    _iqr = q3 - q1
    
    print(f"\n--- {name} Run Length Stats ---")
    print(f"Mean:   {_mean:.2f}")
    print(f"Median: {_median:.2f}")
    print(f"Min:    {_min}")
    print(f"Max:    {_max}")
    print(f"IQR:    {_iqr:.2f} (Q1={q1:.2f}, Q3={q3:.2f})")

def simulation_loop():
    scenarios = load_scenarios()
    
    if SELECTED_SCENARIO_ID not in scenarios:
        print(f"Scenario '{SELECTED_SCENARIO_ID}' not found in {SCENARIO_FILE}")
        return

    scenario_config = scenarios[SELECTED_SCENARIO_ID]
    print(f"Starting {NUM_SIMULATIONS} Simulations for scenario: {scenario_config['description']}")
    
    total_goodies_runs = []
    total_baddies_runs = []
    
    goodies_wins = 0
    baddies_wins = 0
    
    for i in range(NUM_SIMULATIONS):
        # Print first battle for validation
        debug = (i == 0)
        g_runs, b_runs, winner = run_battle(battle_id=i+1, scenario_config=scenario_config, debug_print=debug)
        total_goodies_runs.extend(g_runs)
        total_baddies_runs.extend(b_runs)
        
        if winner == "goodies":
            goodies_wins += 1
        else:
            baddies_wins += 1
            
        if debug:
            pass # Keep debug logic if needed later, or just remove if empty
            
        print(f"Battle {i+1}: Winner = {winner.title()} | Running Score: Goodies {goodies_wins} - Baddies {baddies_wins}")
    
    print("\n=== Simulation Results ===")
    print(f"Final Scorecard: Goodies {goodies_wins} - Baddies {baddies_wins}")
    print_detailed_stats("Player", total_goodies_runs)
    print_detailed_stats("Enemy", total_baddies_runs)

def main():
    simulation_loop()

if __name__ == "__main__":
    main()
