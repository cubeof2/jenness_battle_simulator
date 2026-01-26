from battle_engine import run_battle
import statistics

# Constants
NUM_SIMULATIONS = 1000

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
    print(f"Starting {NUM_SIMULATIONS} Simulations...")
    
    total_goodies_runs = []
    total_baddies_runs = []
    
    for i in range(NUM_SIMULATIONS):
        # Print first battle for validation
        debug = (i == 0)
        g_runs, b_runs = run_battle(battle_id=i+1, debug_print=debug)
        total_goodies_runs.extend(g_runs)
        total_baddies_runs.extend(b_runs)
    
    print("\n=== Simulation Results ===")
    print_detailed_stats("Player", total_goodies_runs)
    print_detailed_stats("Enemy", total_baddies_runs)

def main():
    simulation_loop()

if __name__ == "__main__":
    main()
