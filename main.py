import logging
import argparse
import sys
import json
from pathlib import Path
from typing import List, Dict, Any

from battle_engine import run_battle
from stats import get_stats_lines, get_regression_lines
from constants import SCENARIO_FILE, RESULTS_FILE
from exceptions import ConfigurationError

# Configure Basic Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('battle_sim')

def load_scenarios() -> Dict[str, Any]:
    """Loads and parses the scenario configurations from JSON.

    Returns:
        A dictionary mapping scenario IDs to their configurations.
    """
    path = Path(SCENARIO_FILE)
    if not path.exists():
        logger.error(f"Error: {SCENARIO_FILE} not found.")
        return {}
    
    try:
        with path.open('r') as f:
            data = json.load(f)
        return {s['id']: s for s in data['scenarios']}
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error parsing {SCENARIO_FILE}: {e}")
        return {}

def validate_scenario_config(config: Dict[str, Any]):
    """Checks if the scenario configuration contains all required data.

    Args:
        config: The scenario configuration dictionary to validate.

    Raises:
        ConfigurationError: If required fields are missing or invalid.
    """
    required_keys = ['id', 'description', 'pcs', 'npcs', 'starting_momentum']
    for key in required_keys:
        if key not in config:
            raise ConfigurationError(f"Missing required key '{key}' in scenario config.")

    if not config['pcs']:
        raise ConfigurationError("Scenario must have at least one PC.")
    if not config['npcs']:
        raise ConfigurationError("Scenario must have at least one NPC.")

    # Validate PCs
    for i, pc in enumerate(config['pcs']):
        if 'name' not in pc:
            raise ConfigurationError(f"PC at index {i} is missing a name.")

    # Validate NPCs
    for i, npc in enumerate(config['npcs']):
        for field in ['name', 'hp', 'dt']:
            if field not in npc:
                raise ConfigurationError(f"NPC '{npc.get('name', i)}' is missing field '{field}'.")
        if npc['hp'] <= 0:
            raise ConfigurationError(f"NPC '{npc['name']}' must have HP > 0.")
        if npc['dt'] < 0:
            raise ConfigurationError(f"NPC '{npc['name']}' must have DT >= 0.")


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

    try:
        validate_scenario_config(scenario_config)
    except ConfigurationError as e:
        logger.error(f"Invalid Scenario Configuration: {e}")
        return

    logger.info(f"Starting {num_simulations} Simulations for scenario: {scenario_config['description']}")
    logger.info(f"Logging mode: {log_mode}")
    
    total_pcs_runs = []
    total_npcs_runs = []
    battle_data = []
    
    pcs_wins, npcs_wins = 0, 0
    
    # Configure Root Logger and Handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    root_logger.addHandler(console_handler)
    
    try:
        file_handler = logging.FileHandler(RESULTS_FILE, mode='w', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        root_logger.addHandler(file_handler)
        
        # Write header to file
        file_handler.stream.write(f"Scenario: {scenario_config['description']}\n")
        file_handler.stream.write(f"Simulations: {num_simulations}\n")
        file_handler.stream.write(f"Log Mode: {log_mode}\n\n")
    except IOError as e:
        logger.error(f"Failed to open results file: {e}")
        return
    
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
        from statistics import mean
        battle_data.append({
            'winner': winner,
            'pc_mean_run': mean(pcs_runs) if pcs_runs else 0,
            'npc_mean_run': mean(npcs_runs) if npcs_runs else 0
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
    logger.info(f"\nResults written to {RESULTS_FILE}")

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
