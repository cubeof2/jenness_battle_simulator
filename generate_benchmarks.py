import json
from pathlib import Path

def generate():
    offsets = [5, 7, 9, 10, 11, 13, 15, 17, 20]
    scenarios = []

    # Case 1: 1 Individual PC vs varying sizes of NPC groups
    # Case 2: Group of 5 PCs vs varying sizes of NPC groups
    pc_group_sizes = [1, 5]
    npc_group_sizes = [1, 2, 3, 5, 10, 15]

    for pc_count in pc_group_sizes:
        for npc_count in npc_group_sizes:
            for offset in offsets:
                # We fix Aptitude at 5 for simplicity, adjust DT to meet offset
                apt = 5
                dt = apt + offset
                
                # Naming convention: {pc_count}v{npc_count}_off{offset}
                sid = f"{pc_count}v{npc_count}_off{offset}"
                desc = f"Grid Analysis: {pc_count} PC(s) (Apt 5) vs {npc_count} NPC(s) (DT {dt}). Offset: +{offset}"
                
                pcs = [{"name": f"PC {i+1}", "hp": 4, "aptitude": apt} for i in range(pc_count)]
                npcs = [{"name": f"NPC {i+1}", "hp": 1 if npc_count > 1 else 10, "dt": dt} for i in range(npc_count)]
                
                scenarios.append({
                    "id": sid,
                    "description": desc,
                    "starting_momentum": "pcs",
                    "pcs": pcs,
                    "npcs": npcs
                })

    output = {"scenarios": scenarios}
    with open("benchmarks.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)
    
    print(f"Generated {len(scenarios)} scenarios in benchmarks.json")

if __name__ == "__main__":
    generate()
