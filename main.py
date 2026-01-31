import logging
import argparse
import sys
from battle_engine import run_battle
from stats import get_stats_lines, get_regression_lines
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


def simulation_loop(scenario_id: str, num_simulations: int, log_mode: str = "default"):
    """
    Run battle simulations.
    
    Args:
        scenario_id: ID of the scenario from scenarios.json
        num_simulations: Number of battles to simulate
        log_mode: Logging mode - "default", "short", or "verbose"
            - default: Full first battle details, then just final results
            - short: Only final results summary
            - verbose: Full details for every battle
    """
    scenarios = load_scenarios()
    
    if scenario_id not in scenarios:
        print(f"Scenario '{scenario_id}' not found in {SCENARIO_FILE}")
        return

    scenario_config = scenarios[scenario_id]
    print(f"Starting {num_simulations} Simulations for scenario: {scenario_config['description']}")
    print(f"Logging mode: {log_mode}")
    
    total_pcs_runs = []
    total_npcs_runs = []
    battle_data = []  # Store data for regression: {'winner': str, 'pc_mean_run': float, 'npc_mean_run': float}
    
    pcs_wins = 0
    npcs_wins = 0
    
    # Get root logger to control level globally
    root_logger = logging.getLogger()
    
    # Remove any existing handlers to start fresh
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler - always present
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    root_logger.addHandler(console_handler)
    
    # File handler - writes to simulation_results.txt
    file_handler = logging.FileHandler("simulation_results.txt", mode='w', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    root_logger.addHandler(file_handler)
    
    # Write header to file
    file_handler.stream.write(f"Scenario: {scenario_config['description']}\n")
    file_handler.stream.write(f"Simulations: {num_simulations}\n")
    file_handler.stream.write(f"Log Mode: {log_mode}\n\n")
    file_handler.stream.flush()
    
    for i in range(num_simulations):
        # Set logging level based on mode
        if log_mode == "verbose":
            # All battles get full debug
            root_logger.setLevel(logging.DEBUG)
        elif log_mode == "default" and i == 0:
            # Only first battle gets debug
            root_logger.setLevel(logging.DEBUG)
        else:
            # Short mode or default mode after first battle - suppress battle details
            root_logger.setLevel(logging.WARNING)
            
        pcs_runs, npcs_runs, winner = run_battle(battle_id=i+1, scenario_config=scenario_config)
        total_pcs_runs.extend(pcs_runs)
        total_npcs_runs.extend(npcs_runs)
        
        # Collect detailed stats for regression
        pc_mean = statistics.mean(pcs_runs) if pcs_runs else 0
        npc_mean = statistics.mean(npcs_runs) if npcs_runs else 0
        battle_data.append({
            'winner': winner,
            'pc_mean_run': pc_mean,
            'npc_mean_run': npc_mean
        })
        
        if winner == "pcs":
            pcs_wins += 1
        else:
            npcs_wins += 1
            
        # Battle result line
        battle_result = f"Battle {i+1}: Winner = {winner.upper()} | Running Score: PCs {pcs_wins} - NPCs {npcs_wins}"
        
        # Log based on mode (goes to both console and file when level permits)
        if log_mode == "verbose":
            root_logger.info(battle_result)
        elif log_mode == "default" and i == 0:
            root_logger.info(battle_result)
        # short mode: don't log individual battles
    
    # Generate results summary - always show
    root_logger.setLevel(logging.INFO)
    root_logger.info("\n=== Simulation Results ===")
    root_logger.info(f"Final Scorecard: PCs {pcs_wins} - NPCs {npcs_wins}")
    for line in get_stats_lines("PC", total_pcs_runs):
        root_logger.info(line)
    for line in get_stats_lines("NPC", total_npcs_runs):
        root_logger.info(line)
        
    # Regression Analysis
    for line in get_regression_lines(battle_data):
        root_logger.info(line)
    
    # Clean up file handler
    file_handler.close()
    root_logger.removeHandler(file_handler)
    print(f"\nResults written to simulation_results.txt")

def main():
    parser = argparse.ArgumentParser(description="Jenness Battle Simulator")
    parser.add_argument("--scenario", type=str, default="default_battle", 
                        help="ID of the scenario to run (from scenarios.json)")
    parser.add_argument("--runs", type=int, default=500, 
                        help="Number of simulations to run")
    parser.add_argument("--log", type=str, default="default", choices=["default", "short", "verbose"],
                        help="Logging mode: default (1st battle full, then results), short (results only), verbose (all battles)")
    
    args = parser.parse_args()
    
    simulation_loop(scenario_id=args.scenario, num_simulations=args.runs, log_mode=args.log)

if __name__ == "__main__":
    main()
