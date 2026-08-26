# NEXUS AI REASONING WAR

> **A Next-Generation Cyberpunk Logic & Artificial Intelligence Reasoning Arena**  
> *Integrating Classical Artificial Intelligence, Constraint Satisfaction, Search Optimization, Game Theory, and Machine Learning with Real-Time Explainable AI (XAI).*

---

## 🌟 Project Overview

**NEXUS AI REASONING WAR** is an advanced AI research and interactive game arena engineered in Python. It provides a multi-paradigm testbed for evaluating, visualizing, and explaining algorithmic decision-making across discrete logic puzzles, combinatorial challenges, and adversarial game spaces.

Set in the year 2088 inside the NEXUS Advanced AI Research Facility, players and autonomous AI agents solve complex computational challenges either manually or via autonomous AI solvers featuring live cognitive trace visualization.

---

## 🎯 Problem Statement

Traditional AI reasoning and heuristic search algorithms are often demonstrated through abstract mathematical scripts or static command-line outputs, making it difficult to analyze:
1. Search-space exploration dynamics ($A^*$, Minimax game trees, CSP backtracks).
2. Cognitive decision steps, domain pruning, and deadlock prevention in real time.
3. Comparative optimality between human intuition and formal heuristic solvers.

**NEXUS AI REASONING WAR** bridges this gap by embedding formal AIML algorithms into an interactive, visually rich, and fully explainable cyberpunk software environment.

---

## 🚀 Objectives

- **Algorithmic Rigor**: Implement optimal, production-grade AIML algorithms from scratch with zero dependency bloat.
- **Explainable AI (XAI)**: Provide deep cognitive trace inspection detailing target variables, candidate evaluations, constraint equations, pruning cutoffs, and theoretical foundations.
- **Dual Gameplay Modes**: Support both interactive player modes and automated AI solve modes with step-by-step telemetry.
- **Multi-Modal User Interfaces**: Provide an interactive web dashboard (Streamlit), 2D graphical window (Tkinter), and high-contrast terminal canvas.
- **100% Test Reliability**: Maintain an automated test suite verifying 100% test pass rates across all logic engines and AI solvers.

---

## 🏛️ System Architecture

```
NEXUS AI REASONING WAR
│
├── AI_Agent/                # XAI Engine, Explanation Models & Recorders, Autonomous Agents
│   ├── explanation_models.py # TreeNodes, TimelineSteps, ExplanationSessions
│   ├── explanation_recorder.py# Decoupled Cognitive Trace Recorder
│   ├── nova_agent.py        # Autonomous Companion Agent
│   └── reasoning_tracer.py  # Algorithmic Telemetry Logger
│
├── AI_Algorithms/           # Core Foundational AI Algorithms
│   ├── astar.py             # A* Heuristic Search & Priority Queue
│   ├── bfs.py               # Breadth-First Search Baseline
│   ├── csp_backtracking.py  # CSP with MRV, Forward Checking & LCV
│   ├── decision_theory.py   # Maximum Expected Utility (MEU) Framework
│   ├── forward_chaining.py  # Knowledge Representation & Propositional Chaining
│   ├── graph_algorithms.py  # Edmonds-Karp Minimum Cut & Max Flow
│   ├── minimax.py           # Minimax with Alpha-Beta Pruning
│   └── strips_planner.py    # Classical STRIPS Goal-Oriented Action Planning
│
├── AI_Solvers/              # Instrumented Logic Game Solvers with XAI Recording
│   ├── sudoku_ai.py         # Quantum & Classic Sudoku CSP Solver
│   ├── sokoban_ai.py        # Cyber Sokoban A* Push & Deadlock Solver
│   ├── laser_ai.py          # Laser Mirror Routing Optical Raytrace Solver
│   ├── minesweeper_ai.py    # Circuit Minesweeper Constraint & Inference Solver
│   └── battle_ai.py         # Tactical Battle Arena Minimax Alpha-Beta Solver
│
├── LogicGames/              # Pure Logic Engines with Seed Determinism
│   ├── sudoku_engine.py     # 9x9 Quantum/Classic Matrix Generator & Validator
│   ├── sokoban_engine.py    # Cyber Warehouse Grid Engine with Deadlock Detection
│   ├── laser_engine.py      # Discrete Optical Mirror Grid & Ray Vector Simulator
│   ├── minesweeper_engine.py# High-Voltage Circuit Grid with Life & Mark Systems
│   └── battle_arena_engine.py# 4-in-a-Row Adversarial Matrix Engine
│
├── ML/                      # Native Online Machine Learning Modules
│   ├── kmeans_analyzer.py   # Telemetry Clustering (Player Archetypes)
│   ├── decision_tree_difficulty.py # Dynamic Adaptive Difficulty Scaling
│   ├── ann_predictor.py     # Artificial Neural Network Success Predictor
│   └── ml_pipeline.py       # Real-Time Telemetry & Adaptation Pipeline
│
├── GameEngine/              # Story Mode & RPG Engine
│   ├── world.py, player.py, inventory.py, events.py, missions.py, objects.py
│
├── Missions/                # 10 Story Missions (M01 to M10)
├── UI/                      # Streamlit Web Arena, Desktop Tkinter GUI, Terminal Engine
│   ├── web_game.py          # Unified Cyberpunk Streamlit Web Dashboard & Visualizers
│   ├── desktop_gui.py       # Native 2D Tkinter Graphical Canvas
│   └── terminal_game.py     # High-Performance Terminal ASCII Canvas
│
└── Tests/                   # Automated Unittest Suite (test_all.py)
```

---

## 🎮 Five Core Logic Games

### 1. Sudoku
- **Mechanics**: Traditional 9x9 matrix with 3x3 block borders, notes mode, cell/row/col highlighting, timer, mistake tracker, and hints.
- **AI Integration**: CSP + MRV (Minimum Remaining Values) forward checking and backtracking solver with live step-by-step cognitive trace explanation.

### 2. Cyber Sokoban
- **Mechanics**: Warehouse navigation where the worker pushes energy cores onto target slots.
- **Deadlock Safeguards & Generation**: Procedural goal-derived reverse-pull level generator with deterministic seed control. Proactively detects and prunes corner freezes, wall freezes, 2-box deadlocks, and unreachable target states.

### 3. Laser Mirror Routing
- **Mechanics**: Discrete optical routing where the player and AI rotate diagonal mirrors ($45^\circ / 135^\circ$) to reflect laser beams and energize optical detector cores.
- **Features**: Snell-law optical raytracing, obstacle occlusion, combinatorial rotation search, and reflection angle analytics.

### 4. Circuit Minesweeper
- **Mechanics**: Uncover safe electrical nodes in a high-voltage matrix without shorting fuses.
- **Features**: 3-Life HUD system, 3 marking modes (Reveal, Flag, Question), auto-flood fill, and subset constraint reduction.

### 5. Tactical Battle Arena
- **Mechanics**: Turn-based adversarial matrix game (Connect Four style) competing against the AEGIS tactical AI.
- **Features**: Depth-4 Minimax lookahead, $\alpha$-$\beta$ branch cutoffs, and multi-objective heuristics (attack, defense, center control).

---

## 🏛️ Platform Modules

1. **🎮 Puzzle Arena**: Interactive playable interface for all five games with manual gameplay, undo, hints, AI auto-solve, and cognitive trace inspection.
2. **📊 AI Lab**: Real-time performance dashboard and stress-testing suite benchmarking all five heuristic solvers across state expansions, execution time, and pruning cutoffs.
3. **⚔ Human vs AI**: Direct comparative evaluation arena benchmarking human player moves against optimal AI decision trajectories.
4. **📚 Algorithm Lab**: Theoretical reference and interactive specifications covering CSP, $A^*$ Search, Minimax, Raytracing, Constraint Propagation, and Machine Learning pipelines.

---

## 🔬 Algorithms Used

### 1. CSP + MRV (Minimum Remaining Values)
- **Used In**: Sudoku Engine & Story Vault Missions.
- **Theoretical Foundation**: Formulated as a Constraint Satisfaction Problem $\langle X, D, C \rangle$. Variables are selected via MRV ($|D(v)|$ minimization), values are tested with forward checking, and conflicts trigger systematic backtracking.

### 2. A* Search + Deadlock Detection
- **Used In**: Cyber Sokoban & Pathfinding Navigation.
- **Theoretical Foundation**: Evaluates states using $f(n) = g(n) + h(n)$ with exact Manhattan distance heuristics. Integrated with static and dynamic deadlock pruning to eliminate unpromising push branches.

### 3. Ray Tracing Search & Vector Reflection
- **Used In**: Laser Mirror Routing.
- **Theoretical Foundation**: Traces continuous ray vectors across 2D grid coordinates, computing Snell reflection matrices upon collision with diagonal mirrors ($/$ and $\backslash$). Evaluates combinatorial configurations to maximize detector energization.

### 4. Constraint Satisfaction & Subset Linear Reduction
- **Used In**: Circuit Minesweeper.
- **Theoretical Foundation**: Represents revealed numerical hints as linear equations over binary mine variables: $\sum_{v \in \mathcal{N}(i)} v = c_i$. Solves deterministic single-node relations and applies subset reduction ($S_1 \subset S_2 \implies S_2 - S_1 = c_2 - c_1$) before Bayesian risk ranking.

### 5. Minimax with Alpha-Beta Pruning
- **Used In**: Tactical Battle Arena & Combat Simulations.
- **Theoretical Foundation**: Computes the optimal adversarial move under the Minimax theorem with zero-sum game assumptions. Uses $\alpha$-$\beta$ pruning windows ($\beta \le \alpha$) to prune sub-trees, reducing effective branching factor from $\mathcal{O}(b^d)$ to $\mathcal{O}(b^{d/2})$.

---

## 🧠 Explainable AI (XAI) Module

Every game features an interactive **`[ 🧠 EXPLAIN AI SOLUTION ]`** module powered by the `AI_Agent` telemetry layer:
- **Search Tree Visualizer**: Visual hierarchy displaying explored nodes, pruned branches, backtracks, and optimal paths with interactive node-jump navigation.
- **Interactive Timeline Scrubber**: Step-by-step playback with `[ ⏪ Prev ]`, `[ ▶ Play / ⏸ Pause ]`, `[ ⏩ Next ]`, and `[ 🔄 Reset ]`.
- **Cognitive Decision Inspector**: Detailed breakdowns of selected variables, candidate options evaluated vs rejected, active constraints checked, and theoretical principles.
- **Telemetry Grid**: Complexity class ($\mathcal{O}$ notation), search depth, states evaluated, and pruning efficiency.

---

## 💻 Technology Stack

- **Language**: Python 3.9+
- **Frontend / Web UI**: Streamlit, HTML5 Canvas, Modern CSS3 Glassmorphism, JavaScript
- **Desktop UI**: Tkinter Canvas
- **Terminal UI**: ANSI / ASCII Art High-Contrast Engine
- **Machine Learning**: Native Pure-Python K-Means, Decision Trees, Artificial Neural Networks (Zero external binary dependencies)
- **Testing**: Python `unittest` Framework

---

## 📦 Installation

```bash
# Clone the repository
git clone <repository_url>
cd aiml/Project_3_NEXUS_AI_REASONING_WAR

# Install required dependencies
pip install -r requirements.txt
```

---

## 🕹️ Running Instructions

### 1. Launch Interactive Web Dashboard (Recommended)
```bash
streamlit run UI/web_game.py
# or
python3 main.py --web
```

### 2. Launch Native 2D Desktop Graphical Window
```bash
python3 run_desktop_gui.py
# or
python3 main.py --gui
```

### 3. Launch Cyberpunk Terminal Adventure Game
```bash
python3 run_game.py
# or
python3 main.py --terminal
```

### 4. Run Automated Test Suite
```bash
python3 main.py --test
```

---

## 🧪 Test Results

```
======================================================================
 NEXUS AI REASONING WAR — COMPLETE SYSTEM VERIFICATION TEST SUITE 
======================================================================
Ran 48 tests in 0.496s

OK
======================================================================
 TOTAL TESTS RUN : 48
 SUCCESSES      : 48
 FAILURES       : 0
 ERRORS         : 0
======================================================================
>> ALL SYSTEMS NOMINAL: 100% OF TESTS PASSED SUCCESSFULLY! <<
```

**48/48 Tests Passed (36 V1 Core Tests + 12 V2 Auth/Scoring Tests)**

---

## ⚡ Version 2: Authentication, Player Profiles & Cloud Score System

Version 2 introduces persistent player accounts, deterministic scoring, and Supabase PostgreSQL persistence while preserving 100% of the V1 core game reasoning engines:

### 1. Google OAuth2 Authentication & Guest Mode
- **Guest Mode**: Play immediately without sign-in; scores are saved locally in the active session.
- **Authenticated Mode**: Sign in via Google OAuth2 / OpenID Connect to synchronize scores, lifetime statistics, and personal high scores across devices.
- **Session Persistence**: Authentication state persists cleanly across Streamlit page reruns with full logout control.

### 2. Centralized Game Scoring Engine (`Services/scoring_engine.py`)
- **Deterministic Formulas**:
  - **Sudoku**: $\text{Score} = \max(0, 1000 \times \text{DiffMult} + \text{SpeedBonus} - 150 \times \text{Mistakes} - 200 \times \text{Hints})$
  - **Cyber Sokoban**: $\text{Score} = \max(0, 1200 \times \text{DiffMult} + \text{MoveEfficiency} + \text{PushEfficiency} + \text{SpeedBonus})$
  - **Laser Mirror Routing**: $\text{Score} = \max(0, 1000 \times \text{DiffMult} + \text{RotationEfficiency} + \text{SpeedBonus})$
  - **Circuit Minesweeper**: $\text{Score} = \max(0, 1000 \times \text{DiffMult} + 250 \times \text{Lives} + 15 \times \text{SafeCleared} + \text{SpeedBonus})$
  - **Tactical Battle Arena**: $\text{Score} = \max(0, \text{OutcomeBase} \times \text{DiffMult} + \text{MoveEconomyBonus})$

### 3. Database Persistence (`database/schema.sql`)
- **Schema**: PostgreSQL tables for `players`, `game_scores`, and `game_statistics`.
- **Durable Deduplication**: `game_session_id` UUID with `UNIQUE` constraint ensures a completed game is persisted exactly once.
- **Row Level Security**: Policies isolate player statistics and scores.

### 4. Configuration / Secrets Setup
Add the following to `.streamlit/secrets.toml` or Streamlit Community Cloud Settings:

```toml
# Google OAuth 2.0 Credentials
GOOGLE_CLIENT_ID = "your-google-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your-google-client-secret"
REDIRECT_URI = "https://your-app-url.streamlit.app"

# Supabase PostgreSQL Configuration
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"
```
