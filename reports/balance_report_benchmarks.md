# High-Resolution Balance Report: benchmarks.json

## 🌡️ The Balance Heatmap (Win Rates)
This table shows PC Win Rate (%) for different Offsets and Team Ratios.

| Ratio (NPC vs PC) | Off +5 | Off +7 | Off +9 | Off +10 | Off +11 | Off +13 | Off +15 | Off +17 | Off +20 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1 NPC vs 5 PC** | 100.0% | 100.0% | 100.0% | 98.6% | 93.6% | 48.8% | 6.6% | 0.8% | 0.0% | 
| **2 NPC vs 5 PC** | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 97.0% | 79.2% | 38.0% | 2.4% | 
| **3 NPC vs 5 PC** | 100.0% | 100.0% | 100.0% | 100.0% | 99.8% | 93.2% | 64.0% | 15.2% | 0.8% | 
| **1 NPC vs 1 PC** | 96.8% | 82.5% | 62.8% | 57.0% | 51.7% | 38.5% | 11.6% | 1.5% | 0.0% | 
| **2 NPC vs 1 PC** | 99.9% | 98.7% | 95.1% | 89.5% | 79.8% | 38.8% | 10.7% | 2.5% | 0.1% | 
| **3 NPC vs 1 PC** | 99.9% | 97.4% | 89.4% | 78.6% | 56.2% | 15.9% | 4.3% | 0.2% | 0.0% | 
| **5 NPC vs 1 PC** | 97.6% | 85.8% | 54.2% | 47.8% | 22.0% | 8.0% | 0.4% | 0.0% | 0.0% | 
| **10 NPC vs 1 PC** | 89.8% | 58.0% | 18.8% | 9.0% | 3.8% | 0.2% | 0.0% | 0.0% | 0.0% | 
| **15 NPC vs 1 PC** | 78.0% | 30.0% | 4.4% | 1.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 

## 🔍 High-Resolution Observations

### ⚖️ Group Size Scaling
Do small fights (1v1) behave differently than large ones (5v5) at the same ratio?

| Ratio | PC Size | NPC Size | Avg Win Rate | Avg r |
| :---: | :---: | :---: | :---: | :---: |
| 0.2:1 | 5 | 1 | 60.9% | 0.1665 |
| 0.4:1 | 5 | 2 | 79.6% | 0.1019 |
| 0.6:1 | 5 | 3 | 74.8% | 0.1102 |
| 1.0:1 | 1 | 1 | 22.6% | 0.2106 |
| 1.0:1 | 5 | 5 | 66.8% | 0.1440 |
| 2.0:1 | 1 | 2 | 57.4% | 0.3690 |
| 2.0:1 | 5 | 10 | 57.0% | 0.1902 |
| 3.0:1 | 1 | 3 | 48.7% | 0.3206 |
| 3.0:1 | 5 | 15 | 49.5% | 0.2072 |
| 5.0:1 | 1 | 5 | 35.1% | 0.3013 |
| 10.0:1 | 1 | 10 | 20.0% | 0.2161 |
| 15.0:1 | 1 | 15 | 12.6% | 0.1409 |

## 📋 Raw Data Summary
| Scenario ID | Offset | NPC:PC | Win Rate | r | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `5v1_off5` | +5 | 1:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v2_off5` | +5 | 2:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v3_off5` | +5 | 3:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v1_off5` | +5 | 1:1 | 93.6% | +0.2507 | **Weak Correlation (0.25). The battle is 'Grindy'.** |
| `5v5_off5` | +5 | 5:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v2_off5` | +5 | 2:1 | 99.8% | +0.0746 | **No Correlation (0.07). Victory appears random or decoupled from momentum.** |
| `5v10_off5` | +5 | 10:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v3_off5` | +5 | 3:1 | 99.8% | +0.0848 | **No Correlation (0.08). Victory appears random or decoupled from momentum.** |
| `5v15_off5` | +5 | 15:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v5_off5` | +5 | 5:1 | 97.6% | +0.2764 | **Weak Correlation (0.28). The battle is 'Grindy'.** |
| `1v10_off5` | +5 | 10:1 | 89.8% | +0.3769 | **Healthy** |
| `1v15_off5` | +5 | 15:1 | 78.0% | +0.4072 | **Healthy** |
| `5v1_off7` | +7 | 1:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v2_off7` | +7 | 2:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v3_off7` | +7 | 3:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v1_off7` | +7 | 1:1 | 65.0% | +0.5147 | **Healthy** |
| `5v5_off7` | +7 | 5:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v2_off7` | +7 | 2:1 | 97.4% | +0.3089 | **Healthy** |
| `5v10_off7` | +7 | 10:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v3_off7` | +7 | 3:1 | 94.8% | +0.3056 | **Healthy** |
| `5v15_off7` | +7 | 15:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v5_off7` | +7 | 5:1 | 85.8% | +0.4278 | **Healthy** |
| `1v10_off7` | +7 | 10:1 | 58.0% | +0.5551 | **Healthy** |
| `1v15_off7` | +7 | 15:1 | 30.0% | +0.5031 | **Healthy** |
| `5v1_off9` | +9 | 1:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v2_off9` | +9 | 2:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v3_off9` | +9 | 3:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v1_off9` | +9 | 1:1 | 25.6% | +0.4917 | **Healthy** |
| `5v5_off9` | +9 | 5:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v2_off9` | +9 | 2:1 | 90.6% | +0.3706 | **Healthy** |
| `5v10_off9` | +9 | 10:5 | 99.6% | +0.1391 | **Weak Correlation (0.14). The battle is 'Grindy'.** |
| `1v3_off9` | +9 | 3:1 | 81.4% | +0.4562 | **Healthy** |
| `5v15_off9` | +9 | 15:5 | 97.4% | +0.2911 | **Weak Correlation (0.29). The battle is 'Grindy'.** |
| `1v5_off9` | +9 | 5:1 | 54.2% | +0.5534 | **Healthy** |
| `1v10_off9` | +9 | 10:1 | 18.8% | +0.4154 | **Healthy** |
| `1v15_off9` | +9 | 15:1 | 4.4% | +0.2274 | **Weak Correlation (0.23). The battle is 'Grindy'.** |
| `5v1_off10` | +10 | 1:5 | 98.6% | +0.1935 | **Weak Correlation (0.19). The battle is 'Grindy'.** |
| `5v2_off10` | +10 | 2:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v3_off10` | +10 | 3:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v1_off10` | +10 | 1:1 | 14.4% | +0.3783 | **Healthy** |
| `5v5_off10` | +10 | 5:5 | 99.6% | +0.0980 | **No Correlation (0.10). Victory appears random or decoupled from momentum.** |
| `1v2_off10` | +10 | 2:1 | 82.0% | +0.4598 | **Healthy** |
| `5v10_off10` | +10 | 10:5 | 97.0% | +0.2768 | **Weak Correlation (0.28). The battle is 'Grindy'.** |
| `1v3_off10` | +10 | 3:1 | 72.2% | +0.4900 | **Healthy** |
| `5v15_off10` | +10 | 15:5 | 85.0% | +0.5344 | **Healthy** |
| `1v5_off10` | +10 | 5:1 | 47.8% | +0.5347 | **Healthy** |
| `1v10_off10` | +10 | 10:1 | 9.0% | +0.2822 | **Weak Correlation (0.28). The battle is 'Grindy'.** |
| `1v15_off10` | +10 | 15:1 | 1.0% | +0.1307 | **Weak Correlation (0.13). The battle is 'Grindy'.** |
| `5v1_off11` | +11 | 1:5 | 93.6% | +0.3573 | **Healthy** |
| `5v2_off11` | +11 | 2:5 | 100.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v3_off11` | +11 | 3:5 | 99.8% | +0.0307 | **No Correlation (0.03). Victory appears random or decoupled from momentum.** |
| `1v1_off11` | +11 | 1:1 | 4.8% | +0.2597 | **Weak Correlation (0.26). The battle is 'Grindy'.** |
| `5v5_off11` | +11 | 5:5 | 98.6% | +0.1221 | **Weak Correlation (0.12). The battle is 'Grindy'.** |
| `1v2_off11` | +11 | 2:1 | 74.4% | +0.5266 | **Healthy** |
| `5v10_off11` | +11 | 10:5 | 85.2% | +0.5298 | **Healthy** |
| `1v3_off11` | +11 | 3:1 | 54.6% | +0.4822 | **Healthy** |
| `5v15_off11` | +11 | 15:5 | 57.8% | +0.6923 | **CRITICAL** |
| `1v5_off11` | +11 | 5:1 | 22.0% | +0.4766 | **Healthy** |
| `1v10_off11` | +11 | 10:1 | 3.8% | +0.2494 | **Weak Correlation (0.25). The battle is 'Grindy'.** |
| `1v15_off11` | +11 | 15:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v1_off13` | +13 | 1:5 | 48.8% | +0.5829 | **Healthy** |
| `5v2_off13` | +13 | 2:5 | 97.0% | +0.1626 | **Weak Correlation (0.16). The battle is 'Grindy'.** |
| `5v3_off13` | +13 | 3:5 | 93.2% | +0.2338 | **Weak Correlation (0.23). The battle is 'Grindy'.** |
| `1v1_off13` | +13 | 1:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v5_off13` | +13 | 5:5 | 77.0% | +0.4781 | **Healthy** |
| `1v2_off13` | +13 | 2:1 | 47.6% | +0.5495 | **Healthy** |
| `5v10_off13` | +13 | 10:5 | 30.0% | +0.5978 | **Healthy** |
| `1v3_off13` | +13 | 3:1 | 26.6% | +0.4692 | **Healthy** |
| `5v15_off13` | +13 | 15:5 | 5.2% | +0.3466 | **Healthy** |
| `1v5_off13` | +13 | 5:1 | 8.0% | +0.3524 | **Healthy** |
| `1v10_off13` | +13 | 10:1 | 0.2% | +0.0663 | **No Correlation (0.07). Victory appears random or decoupled from momentum.** |
| `1v15_off13` | +13 | 15:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v1_off15` | +15 | 1:5 | 6.6% | +0.2832 | **Weak Correlation (0.28). The battle is 'Grindy'.** |
| `5v2_off15` | +15 | 2:5 | 79.2% | +0.2746 | **Weak Correlation (0.27). The battle is 'Grindy'.** |
| `5v3_off15` | +15 | 3:5 | 64.0% | +0.3650 | **Healthy** |
| `1v1_off15` | +15 | 1:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v5_off15` | +15 | 5:5 | 23.2% | +0.4090 | **Healthy** |
| `1v2_off15` | +15 | 2:1 | 20.0% | +0.5175 | **Healthy** |
| `5v10_off15` | +15 | 10:5 | 1.4% | +0.1680 | **Weak Correlation (0.17). The battle is 'Grindy'.** |
| `1v3_off15` | +15 | 3:1 | 8.6% | +0.3906 | **Healthy** |
| `5v15_off15` | +15 | 15:5 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v5_off15` | +15 | 5:1 | 0.4% | +0.0901 | **No Correlation (0.09). Victory appears random or decoupled from momentum.** |
| `1v10_off15` | +15 | 10:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v15_off15` | +15 | 15:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v1_off17` | +17 | 1:5 | 0.8% | +0.0812 | **No Correlation (0.08). Victory appears random or decoupled from momentum.** |
| `5v2_off17` | +17 | 2:5 | 38.0% | +0.3767 | **Healthy** |
| `5v3_off17` | +17 | 3:5 | 15.2% | +0.3044 | **Healthy** |
| `1v1_off17` | +17 | 1:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v5_off17` | +17 | 5:5 | 3.0% | +0.1890 | **Weak Correlation (0.19). The battle is 'Grindy'.** |
| `1v2_off17` | +17 | 2:1 | 5.0% | +0.2925 | **Weak Correlation (0.29). The battle is 'Grindy'.** |
| `5v10_off17` | +17 | 10:5 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v3_off17` | +17 | 3:1 | 0.4% | +0.2069 | **Weak Correlation (0.21). The battle is 'Grindy'.** |
| `5v15_off17` | +17 | 15:5 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v5_off17` | +17 | 5:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v10_off17` | +17 | 10:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v15_off17` | +17 | 15:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v1_off20` | +20 | 1:5 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v2_off20` | +20 | 2:5 | 2.4% | +0.1035 | **Weak Correlation (0.10). The battle is 'Grindy'.** |
| `5v3_off20` | +20 | 3:5 | 0.8% | +0.0575 | **No Correlation (0.06). Victory appears random or decoupled from momentum.** |
| `1v1_off20` | +20 | 1:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v5_off20` | +20 | 5:5 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v2_off20` | +20 | 2:1 | 0.2% | +0.2207 | **Weak Correlation (0.22). The battle is 'Grindy'.** |
| `5v10_off20` | +20 | 10:5 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v3_off20` | +20 | 3:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `5v15_off20` | +20 | 15:5 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v5_off20` | +20 | 5:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v10_off20` | +20 | 10:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
| `1v15_off20` | +20 | 15:1 | 0.0% | +0.0000 | **No Correlation (0.00). Victory appears random or decoupled from momentum.** |
