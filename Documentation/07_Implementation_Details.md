# 07. IMPLEMENTATION DETAILS

## 1. Programming Environment & Technology Stack
- **Programming Language**: Python 3.9+ (Standard Library Architecture)
- **GUI & Graphics Frameworks**:
  - Native Tkinter Desktop 2D Canvas (`UI/desktop_gui.py`)
  - ANSI/Curses Cyberpunk Terminal Canvas (`UI/terminal_game.py`)
  - Streamlit Interactive Web Canvas (`UI/web_game.py`)
- **Mathematical & Symbolic Engines**: Pure Python standard library implementation with zero external package locks.
- **Testing Framework**: Standard `unittest` with comprehensive test runner (`Tests/test_all.py`).

---

## 2. Directory & Module Organization
```
aiml/Project_3_NEXUS_AI_REASONING_WAR/
├── main.py                     # Unified multi-modal entry point
├── run_game.py                 # Primary terminal interactive launcher
├── run_desktop_gui.py          # Native 2D desktop window launcher
├── run_web.py                  # Streamlit web canvas launcher
├── GAME_DESIGN_DOCUMENT.md     # Full design specifications & world lore
├── README.md                   # Project overview & quickstart guide
├── GameEngine/                 # World, player, objects, inventory, missions, events
├── AI_Algorithms/              # A*, BFS, CSP, Forward Chaining, Minimax, MEU, STRIPS, Min-Cut
├── ML/                         # K-Means, Decision Tree, ANN, ML Pipeline
├── Missions/                   # 10 full playable missions
├── AI_Agent/                   # NOVA Companion, Autonomous Solver, Reasoning Tracer
├── UI/                         # Visual frames, ASCII art, GUI, and Web renderers
├── Dataset/                    # Telemetry schema, player CSV, scenario blueprints
├── Models/                     # K-Means centroids, Decision Tree rules, ANN weights
├── Documentation/              # 01_Abstract to 11_References
└── Tests/                      # Automated test suite (test_all.py)
```

---

## 3. Mission Implementations (10 Playable Challenges)
1. **M01: Restore AI Core Power Conduits** ($A^*$ vs BFS Pathfinding in AI Core Garden)
2. **M02: Digital Crime Investigation** (Forward Chaining Logic Inference in Digital Forensic Lab)
3. **M03: Quantum Security Vault** (5-variable CSP Backtracking & Forward Checking in Quantum Lab)
4. **M04: Combat Simulation ARES-7** (Minimax with $\alpha$-$\beta$ Pruning in Robot Training Arena)
5. **M05: Network Infection Containment** (Edmonds-Karp Minimum Cut in Network Control Center)
6. **M06: Recover Fragmented Memory** (Semantic Ontologies in AI Core Garden)
7. **M07: Strategic Ethical Containment** (Decision Theory & Maximum Expected Utility in Final Nexus)
8. **M08: Automated Drone Evacuation** (STRIPS Action Planning in Robot Training Arena)
9. **M09: Adaptive Machine Learning Test** (Adversarial Boundary Perturbation in Quantum Lab)
10. **M10: The Grand Finale NEXUS Prime** (Multi-Paradigm Universal Synthesis in Final Nexus Chamber)
