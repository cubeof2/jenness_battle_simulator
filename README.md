# Jenness Battle Simulator

A robust momentum-based statistical simulation engine designed to test, balance, and analyze combat encounters for Jenness' tabletop RPG system.

## ⚔️ Purpose
The Jenness Battle Simulator allows game designers to run thousands of simulated battles in seconds. Its primary goal is to determine the statistical "fairness" and "flow" of combat encounters, helping you identify if a boss is too lethal, if players have enough resources, or if certain mechanics (like expertise or banes) are having the intended impact on gameplay.

---

## 🚀 Beginner's Guide (How to Run This)
If you've never used GitHub or written a line of code, follow these steps to see the simulator in action:

1. **Install Python**: Go to [Python.org](https://www.python.org/) and download the latest version for your operating system. During installation, **make sure to check the box that says "Add Python to PATH"**.
2. **Download the Code**: 
   - Click the green **"<> Code"** button at the top of this GitHub page.
   - Select **"Download ZIP"**.
   - Extract the ZIP file to a folder on your computer (e.g., your Desktop).
3. **Open a Command Window**:
   - **On Windows**:
     - Open the folder where you extracted the files.
     - Click in the "Address Bar" at the very top of the folder window (where it shows the folder path).
     - Type `cmd` and press **Enter**.
   - **On macOS (Apple)**:
     - Open the "Terminal" app (you can find it in Applications > Utilities, or search for it with Command + Space).
     - Type `cd` followed by a space.
     - Drag your extracted folder from the Finder directly into the Terminal window. The path will appear automatically.
     - Press **Enter**.
4. **Run the Battle**:
   - In that window, type the following and press **Enter**:
     ```bash
     python3 main.py
     ```
   - *Note: On some systems, you might need to use `python` instead of `python3`.*

---

## 🔧 How It Works

### 1. The Configuration (`scenarios.json`)
The simulator depends entirely on this file. It defines:
- **PCs (Players)**: Their HP, Aptitude, and whether they have "Expertise" in Attack or Defense.
- **NPCs (Enemies)**: Their HP and Difficulty Threshold (DT) which players must roll against to hit them.
- **Starting Momentum**: Who begins the fight with the upper hand.

You can add new scenarios or modify existing ones by opening this file in a text editor like Notepad.

### 2. The Core Mechanics
The engine simulates turns using the following logic:
- **The Roll**: `d20 + Aptitude + Boons - Banes`
- **Triumph**: A natural 20 is an automatic critical success.
- **Clean Success**: Beating the target's DT by 3 or more.
- **Setback**: Rolling within 2 points of the target (barely succeeding/failing).
- **Catastrophe**: Failing by 10 or more.

### 3. The Output (`simulation_results.txt`)
Every time you run a simulation, a file named `simulation_results.txt` is created or updated. This file contains the full log of the battles and the final statistical breakdown.

---

## 📊 Interpreting the Results

### Run Length Stats
This measures how many "successes" a side gets in a row. 
- **High Mean Run**: Indicates a side is "dominating" the flow of battle.
- **High Max Run**: Shows potential for "death spirals" where one side can't catch a break.

### Histograms
The visual bars show the distribution of combat flow. If the histogram is heavily weighted toward "1", the battle is "swingy" and chaotic. If it has many longer runs, the battle is more predictable and one-sided.

### Regression Analysis
This is your **Balance Stress-Test**. It measures how much "Momentum Streaks" decide the winner versus the actual stats (HP/Defense) of your characters.

- **High Correlation (>0.6) - "Snowbally"**: One side getting a lucky streak effectively ends the fight. This suggests momentum is too powerful or character HP is too low.
- **Moderate Correlation (0.3 - 0.6) - "Balanced"**: Momentum helps, but a durable team can survive an enemy's "hot streak" and eventually grind out a win. This is usually the "sweet spot" for tactical play.
- **Low Correlation (<0.3) - "Grindy/Static"**: Combat flow doesn't matter. The winner is likely decided by who has the biggest raw numbers (like massive HP), and "tactical streaks" aren't impactful.

---

## ⌨️ Advanced Commands (CLI)
If you want to customize your runs, use these options in the command window:

- **Run a specific scenario**: `python main.py --scenario small_skirmish`
- **Change number of battles**: `python main.py --runs 1000`
- **Change detail level**: 
  - `python main.py --log short` (Just the final stats)
  - `python main.py --log verbose` (Every single die roll for every battle)

---

## 🧪 Testing & Quality
To ensure the simulation logic remains accurate, you can run the automated test suite:

1. **Install Test Dependencies**:
   ```bash
   pip install pytest
   ```
2. **Run Tests**:
   ```bash
   python -m pytest
   ```

## 📊 Benchmarking & Sensitivity
The project includes a bulk-runner to analyze how robust the momentum system is across many different scenarios.

- **Run All Benchmarks**:
  ```bash
  python bulk_run.py
  ```
- **View Results**: Detailed markdown reports are generated in the `reports/` directory, showing win rates, momentum correlation (r), and Difficulty-Aptitude offsets.

### 🎯 The Designer's Handbook: Rules of Thumb
The following table shows the **Offset** (DT - Aptitude) required for a **Balanced (50-60% WR)** encounter:

| Encounter Type | Team Composition | Target Offset (DT - Apt) |
| :--- | :---: | :---: |
| **Boss Fight** | 1 NPC vs 5 PCs | **+13 to +14** |
| **Symmetric** | 5 NPCs vs 5 PCs | **+11 to +12** |
| **Duel** | 1 NPC vs 1 PC | **+10 to +11** |
| **Horde** | 10 NPCs vs 1 PC | **+7 to +8** |
| **Impossible** | 15 NPCs vs 1 PC | **+5 or lower** |

#### 💡 Pro Tips for Designers:
- **Safety in Numbers**: Fights with more total participants (e.g., 5v5) are **more stable** for players. If you want a predictable tactical experience, add more units to both sides.
- **The "Lone Hero" Risk**: A 1v1 duel is highly volatile. A single "Catastrophe" can end the fight instantly. In group combat, the momentum system creates a "buffer" that absorbs bad luck.
- **Scaling Difficulty**: If you want to make an encounter "Hard" (30% WR), simply add **+2** to the target offsets above.
