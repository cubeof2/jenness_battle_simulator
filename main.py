import logging
import argparse
import sys
from battle_engine import run_battle
from typing import List, Dict, Any
import statistics
import json
import os

# Configure Basic Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('battle_sim')

SCENARIO_FILE = "scenarios.json"

def load_scenarios() -> Dict[str, Any]:
    if not os.path.exists(SCENARIO_FILE):
        print(f"Error: {SCENARIO_FILE} not found.")
        return {}
    
    with open(SCENARIO_FILE, 'r') as f:
        data = json.load(f)
        
    return {s['id']: s for s in data['scenarios']}

def print_detailed_stats(name: str, data: List[int]):
    if not data:
        print(f"{name}: No data collected.")
        return
        
    _min = min(data)
    _max = max(data)
    _mean = statistics.mean(data)
    _median = statistics.median(data)
    
    # Calculate IQR
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

def simulation_loop(scenario_id: str, num_simulations: int):
    scenarios = load_scenarios()
    
    if scenario_id not in scenarios:
        print(f"Scenario '{scenario_id}' not found in {SCENARIO_FILE}")
        return

    scenario_config = scenarios[scenario_id]
    print(f"Starting {num_simulations} Simulations for scenario: {scenario_config['description']}")
    
    total_pcs_runs = []
    total_npcs_runs = []
    
    pcs_wins = 0
    npcs_wins = 0
    
    # Get root logger to control level globally
    root_logger = logging.getLogger()
    
    for i in range(num_simulations):
        # Set logging level: DEBUG for first run, INFO for subsequent
        if i == 0:
            root_logger.setLevel(logging.DEBUG)
        else:
            root_logger.setLevel(logging.INFO)
            
        pcs_runs, npcs_runs, winner = run_battle(battle_id=i+1, scenario_config=scenario_config)
        total_pcs_runs.extend(pcs_runs)
        total_npcs_runs.extend(npcs_runs)
        
        if winner == "pcs":
            pcs_wins += 1
        else:
            npcs_wins += 1
            
        # Log result using INFO level so it always shows
        # Note: Since we switch to INFO level for subsequent runs, strictly INFO logs appeal.
        # But for the FIRST run (DEBUG level), INFO logs also appear.
        root_logger.info(f"Battle {i+1}: Winner = {winner.upper()} | Running Score: PCs {pcs_wins} - NPCs {npcs_wins}")
    
    print("\n=== Simulation Results ===")
    print(f"Final Scorecard: PCs {pcs_wins} - NPCs {npcs_wins}")
    print_detailed_stats("PC", total_pcs_runs)
    print_detailed_stats("NPC", total_npcs_runs)

def main():
    parser = argparse.ArgumentParser(description="Jenness Battle Simulator")
    parser.add_argument("--scenario", type=str, default="default_battle", 
                        help="ID of the scenario to run (from scenarios.json)")
    parser.add_argument("--runs", type=int, default=500, 
                        help="Number of simulations to run")
    
    args = parser.parse_args()
    
    simulation_loop(scenario_id=args.scenario, num_simulations=args.runs)

if __name__ == "__main__":
    main()
