import logging
import json
import argparse
from pathlib import Path
from statistics import mean
from typing import List, Dict, Any

from battle_engine import run_battle
from stats import get_regression_lines

# Define a minimal logging config to avoid cluttering the console
logging.basicConfig(level=logging.WARNING, format='%(message)s')
logger = logging.getLogger('bulk_runner')

def parse_regression_info(regression_lines: List[str]) -> Dict[str, str]:
    """Extracts r-value and interpretation from regression lines."""
    info = {"r": "N/A", "label": "N/A"}
    for i, line in enumerate(regression_lines):
        if "Run Length Difference" in line:
            if i + 1 < len(regression_lines) and "Correlation (r):" in regression_lines[i+1]:
                info["r"] = regression_lines[i+1].split(":")[-1].strip()
        
        if "Interpretation:" in line:
            if i + 1 < len(regression_lines):
                full_label = regression_lines[i+1].strip()
                if ":" in full_label:
                    info["label"] = full_label.split(":")[0].strip()
                else:
                    info["label"] = full_label
    return info

def run_benchmarks(scenario_file="scenarios.json", sim_count=200):
    """Runs all scenarios and generates a robustness & sensitivity report."""
    print(f"--- Starting Bulk Benchmark on {scenario_file} ---")
    print(f"--- {sim_count} runs per scenario ---")
    
    path = Path(scenario_file)
    if not path.exists():
        print(f"Error: {scenario_file} not found.")
        return

    with path.open('r') as f:
        data = json.load(f)
        scenarios = {s['id']: s for s in data['scenarios']}
    
    results = []
    
    for sid, config in scenarios.items():
        print(f"Simulating: {sid}...")
        
        pcs_wins = 0
        battle_data = []
        
        for i in range(sim_count):
            pcs_runs, npcs_runs, winner = run_battle(i, config)
            if winner == "pcs":
                pcs_wins += 1
            
            battle_data.append({
                'winner': winner,
                'pc_mean_run': mean(pcs_runs) if pcs_runs else 0,
                'npc_mean_run': mean(npcs_runs) if npcs_runs else 0
            })
            
        win_rate = (pcs_wins / sim_count) * 100
        reg_info = parse_regression_info(get_regression_lines(battle_data))
        
        # Calculate Offset: Average NPC DT - Average PC Aptitude
        avg_apt = mean([p.get('aptitude', 5) for p in config['pcs']]) if config['pcs'] else 5
        avg_dt = mean([n.get('dt', 12) for n in config['npcs']]) if config['npcs'] else 12
        offset = avg_dt - avg_apt
        
        # Calculate Ratio: NPC count / PC count
        ratio = len(config['npcs']) / len(config['pcs']) if config['pcs'] else 0

        results.append({
            "id": sid,
            "win_rate": win_rate,
            "r": reg_info["r"],
            "label": reg_info["label"],
            "offset": offset,
            "ratio": ratio,
            "pc_count": len(config['pcs']),
            "npc_count": len(config['npcs']),
            "description": config["description"]
        })

    # Generate Report
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    
    report_path = report_dir / f"balance_report_{path.stem}.md"
    
    with report_path.open("w", encoding="utf-8") as f:
        f.write(f"# High-Resolution Balance Report: {scenario_file}\n\n")
        
        f.write("## 🌡️ The Balance Heatmap (Win Rates)\n")
        f.write("This table shows PC Win Rate (%) for different Offsets and Team Ratios.\n\n")
        
        # Group and build table
        offsets = sorted(list(set([r['offset'] for r in results])))
        ratios = sorted(list(set([r['ratio'] for r in results])))
        
        f.write("| Ratio (NPC vs PC) | " + " | ".join([f"Off +{o}" for o in offsets]) + " |\n")
        f.write("| :--- | " + " | ".join([":---:" for _ in offsets]) + " |\n")
        
        for ratio in ratios:
            # Find a representative scenario to get counts
            sample = [r for r in results if r['ratio'] == ratio][0]
            label = f"**{sample['npc_count']} NPC vs {sample['pc_count']} PC**"
            
            line = f"| {label} | "
            for offset in offsets:
                matches = [r for r in results if r['offset'] == offset and r['ratio'] == ratio]
                if matches:
                    avg_wr = mean([m['win_rate'] for m in matches])
                    line += f"{avg_wr:>.1f}% | "
                else:
                    line += "--- | "
            f.write(line + "\n")

        f.write("\n## 🔍 High-Resolution Observations\n\n")
        
        f.write("### ⚖️ Group Size Scaling\n")
        f.write("Do small fights (1v1) behave differently than large ones (5v5) at the same ratio?\n\n")
        f.write("| Ratio | PC Size | NPC Size | Avg Win Rate | Avg r |\n")
        f.write("| :---: | :---: | :---: | :---: | :---: |\n")
        
        for ratio in ratios:
            # Get unique counts for this ratio
            configs = sorted(list(set([(r['pc_count'], r['npc_count']) for r in results if r['ratio'] == ratio])))
            for pc_sz, npc_sz in configs:
                matches = [r for r in results if r['pc_count'] == pc_sz and r['npc_count'] == npc_sz]
                avg_wr = mean([m['win_rate'] for m in matches])
                try:
                    avg_r = mean([float(m['r']) for m in matches if m['r'] != 'N/A'])
                except:
                    avg_r = 0.0
                f.write(f"| {ratio:.1f}:1 | {pc_sz} | {npc_sz} | {avg_wr:.1f}% | {avg_r:.4f} |\n")

        f.write("\n## 📋 Raw Data Summary\n")
        f.write("| Scenario ID | Offset | NPC:PC | Win Rate | r | Status |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :--- |\n")
        for r in sorted(results, key=lambda x: (x['offset'], x['ratio'])):
            f.write(f"| `{r['id']}` | +{r['offset']} | {r['npc_count']}:{r['pc_count']} | {r['win_rate']:.1f}% | {r['r']} | **{r['label']}** |\n")

    print(f"\nBenchmark Complete! View the results in: {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk runner for balance benchmarks")
    parser.add_argument("--file", type=str, default="benchmarks.json", help="Scenario JSON file")
    parser.add_argument("--runs", type=int, default=500, help="Simulations per scenario")
    args = parser.parse_args()
    
    run_benchmarks(scenario_file=args.file, sim_count=args.runs)
