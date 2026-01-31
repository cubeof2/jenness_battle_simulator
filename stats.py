import statistics
from typing import List, Dict
from collections import Counter

def get_histogram_lines(name: str, data: List[int], max_bar_width: int = 40) -> List[str]:
    """Generate a text-based histogram as a list of strings."""
    lines = []
    if not data:
        return lines
    
    counts = Counter(data)
    max_val = max(counts.keys())
    max_count = max(counts.values())
    
    lines.append(f"\n--- {name} Run Length Histogram ---")
    
    for length in range(1, max_val + 1):
        count = counts.get(length, 0)
        bar_length = int((count / max_count) * max_bar_width) if max_count > 0 else 0
        bar = "█" * bar_length
        percentage = (count / len(data)) * 100
        lines.append(f"{length:2d}: {bar:<{max_bar_width}} ({count:4d}, {percentage:5.1f}%)")
    
    return lines

def get_regression_lines(battle_data: List[Dict]) -> List[str]:
    """
    Perform regression analysis on run length vs win outcome.
    
    battle_data: List of dicts with keys: 'winner', 'pc_mean_run', 'npc_mean_run'
    """
    lines = []
    lines.append("\n=== Regression Analysis: Run Length vs Win ===")
    
    if len(battle_data) < 10:
        lines.append("Insufficient data for regression (need at least 10 battles)")
        return lines
    
    # Extract data
    pc_wins = [1 if b['winner'] == 'pcs' else 0 for b in battle_data]
    pc_mean_runs = [b['pc_mean_run'] for b in battle_data]
    npc_mean_runs = [b['npc_mean_run'] for b in battle_data]
    
    # Simple correlation calculation (Pearson)
    def pearson_correlation(x: List[float], y: List[float]) -> float:
        n = len(x)
        if n == 0:
            return 0.0
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denom_x = sum((xi - mean_x) ** 2 for xi in x) ** 0.5
        denom_y = sum((yi - mean_y) ** 2 for yi in y) ** 0.5
        
        if denom_x == 0 or denom_y == 0:
            return 0.0
        return numerator / (denom_x * denom_y)
    
    # Simple linear regression (slope and intercept)
    def linear_regression(x: List[float], y: List[float]) -> tuple:
        n = len(x)
        if n == 0:
            return 0.0, 0.0
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = sum((xi - mean_x) ** 2 for xi in x)
        
        if denominator == 0:
            return 0.0, mean_y
        
        slope = numerator / denominator
        intercept = mean_y - slope * mean_x
        return slope, intercept
    
    # Correlation: PC mean run vs PC win
    corr_pc = pearson_correlation(pc_mean_runs, pc_wins)
    slope_pc, intercept_pc = linear_regression(pc_mean_runs, pc_wins)
    
    # Correlation: NPC mean run vs PC win (should be negative)
    corr_npc = pearson_correlation(npc_mean_runs, pc_wins)
    slope_npc, intercept_npc = linear_regression(npc_mean_runs, pc_wins)
    
    # Correlation: Run length difference vs PC win
    run_diff = [p - n for p, n in zip(pc_mean_runs, npc_mean_runs)]
    corr_diff = pearson_correlation(run_diff, pc_wins)
    slope_diff, intercept_diff = linear_regression(run_diff, pc_wins)
    
    lines.append("\nPC Mean Run Length vs PC Win:")
    lines.append(f"  Correlation (r): {corr_pc:+.4f}")
    lines.append(f"  Linear Model:    P(PC Win) = {intercept_pc:.4f} + {slope_pc:+.4f} * PC_Mean_Run")
    
    lines.append("\nNPC Mean Run Length vs PC Win:")
    lines.append(f"  Correlation (r): {corr_npc:+.4f}")
    lines.append(f"  Linear Model:    P(PC Win) = {intercept_npc:.4f} + {slope_npc:+.4f} * NPC_Mean_Run")
    
    lines.append("\nRun Length Difference (PC - NPC) vs PC Win:")
    lines.append(f"  Correlation (r): {corr_diff:+.4f}")
    lines.append(f"  Linear Model:    P(PC Win) = {intercept_diff:.4f} + {slope_diff:+.4f} * (PC_Run - NPC_Run)")
    
    # Interpretation
    lines.append("\nInterpretation:")
    if abs(corr_diff) > 0.3:
        lines.append(f"  Strong {'positive' if corr_diff > 0 else 'negative'} correlation between run length difference and PC victory.")
    elif abs(corr_diff) > 0.1:
        lines.append(f"  Moderate {'positive' if corr_diff > 0 else 'negative'} correlation between run length difference and PC victory.")
    else:
        lines.append("  Weak/No significant correlation - run length difference does not strongly predict winner.")
    
    return lines

def get_stats_lines(name: str, data: List[int]) -> List[str]:
    """Generate stats as a list of strings for both printing and file output."""
    lines = []
    if not data:
        lines.append(f"{name}: No data collected.")
        return lines
        
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
    
    lines.append(f"\n--- {name} Run Length Stats ---")
    lines.append(f"Mean:   {_mean:.2f}")
    lines.append(f"Median: {_median:.2f}")
    lines.append(f"Min:    {_min}")
    lines.append(f"Max:    {_max}")
    lines.append(f"IQR:    {_iqr:.2f} (Q1={q1:.2f}, Q3={q3:.2f})")
    
    # Add histogram
    lines.extend(get_histogram_lines(name, data))
    
    return lines
