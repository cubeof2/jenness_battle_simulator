# Robustness & Sensitivity Analysis Report

## Scenario Summary
| Scenario ID | Offset (DT-Apt) | Win Rate | Correlation (r) | Status | Description |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `stress_horde` | +5.0 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** | ROBUSTNESS: 1 PC vs 12 Minions. Tests friction impact. |
| `offset_7_high` | +7.0 | 96.5% | +0.2836 | **Weak Correlation (0.28). The battle is 'Grindy'.** | OFFSET 7: (Apt 15, DT 22). Testing if high raw numbers change the feel. |
| `offset_7_low` | +7.0 | 97.0% | +0.2064 | **Weak Correlation (0.21). The battle is 'Grindy'.** | OFFSET 7: (Apt 5, DT 12). Base baseline. |
| `offset_10_high` | +10.0 | 58.5% | +0.4889 | **Healthy** | OFFSET 10: (Apt 10, DT 20). Balanced/Moderate at higher target. |
| `offset_10_low` | +10.0 | 59.5% | +0.6258 | **CRITICAL** | OFFSET 10: (Apt 5, DT 15). Balanced/Moderate difficulty. |
| `offset_13_high` | +13.0 | 16.5% | +0.4014 | **Healthy** | OFFSET 13: (Apt 7, DT 20). Difficult at higher target. |
| `offset_13_low` | +13.0 | 17.0% | +0.3839 | **Healthy** | OFFSET 13: (Apt 5, DT 18). Difficult. |
| `stress_the_wall` | +15.0 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** | ROBUSTNESS: High Defense Boss. Tests momentum vs high stats. |

## 🔍 Analysis & Observations

### ⚖️ Offset Sensitivity (DT minus Aptitude)
This table shows how the relationship between player skill and difficulty drives the outcome.

| Offset | Scenario Count | Avg Win Rate | Avg Correlation (r) |
| :---: | :---: | :---: | :---: |
| +5.0 | 1 | +100.0% | 0.0000 |
| +7.0 | 2 | +96.8% | 0.2450 |
| +10.0 | 2 | +59.0% | 0.5574 |
| +13.0 | 2 | +16.8% | 0.3926 |
| +15.0 | 1 | +0.0% | 0.0000 |

> [!NOTE]
> If scenarios with the same offset have different win rates, it suggests the system has secondary variables (like expertise or HP pools) that matter more than raw numbers at that level.

### 🌪️ Robustness Stress-Tests
- **The Wall**: If Correlation is low (< 0.2), momentum doesn't matter against high stats. If it's high, lucky streaks can bypass hard stats.
- **Glass Cannons**: High correlation (Snowbally) is expected here; the question is if it reaches 1.0 (pure luck).
- **The Horde**: Checks if Friction properly limits enemy advantage streaks.
