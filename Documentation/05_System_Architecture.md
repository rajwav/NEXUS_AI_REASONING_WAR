# 05. SYSTEM ARCHITECTURE

## 1. High-Level Architectural Model
The architecture of **NEXUS AI REASONING WAR** follows a modular, decoupled Layered Architecture structured into six core subsystems:

```
+===================================================================================+
|                             USER INTERFACE LAYER                                  |
|   [Native Desktop 2D Canvas]  |  [Cyberpunk Terminal Engine]  |  [Web Canvas UI]  |
+===================================================================================+
                                         |
                                         v
+===================================================================================+
|                              GAME ENGINE LAYER                                    |
|   - World & Sectors (world.py)           - Player & Telemetry (player.py)         |
|   - Objects & Terminals (objects.py)     - Inventory & Crafting (inventory.py)    |
|   - Event Broker (events.py)             - Interaction Handler (interaction.py)   |
|   - Mission Progression (missions.py)                                             |
+===================================================================================+
                 |                                               |
                 v                                               v
+================================+               +================================+
|      AI ALGORITHM SUITE        |               |    MACHINE LEARNING ENGINE     |
|  - A* Search & BFS             |               |  - K-Means Player Archetyping  |
|  - CSP Backtracking (MRV + FC) |               |  - Decision Tree Difficulty    |
|  - Forward Chaining Inference  |               |  - ANN Success Predictor (MLP) |
|  - Minimax with Alpha-Beta     |               |  - Online ML Pipeline Stream   |
|  - Decision Theory (MEU)       |               +================================+
|  - STRIPS Action Planner       |                               |
|  - Edmonds-Karp Min-Cut        |                               v
+================================+               +================================+
                 |                               |       AI COMPANION AGENT       |
                 +------------------------------>|  - NOVA Personality & Advisory |
                                                 |  - Autonomous Physical Solver  |
                                                 |  - Reasoning Step Tracer       |
                                                 +================================+
```

---

## 2. Subsystem Descriptions

### 2.1 Game Engine Subsystem (`GameEngine/`)
- **World (`world.py`)**: Maintains 2D matrix grids across the 6 interconnected sectors, hazard flags, and bidirectional door portals.
- **Player (`player.py`)**: Tracks coordinates $(x, y)$, heading, health, energy, and telemetry streams.
- **Objects & Inventory (`objects.py`, `inventory.py`)**: Implements physical objects (Terminals, Servers, Lasers, Cores) and a multi-slot inventory with item combinations.
- **Event Bus (`events.py`)**: Dispatches asynchronous game events (movement, inspection, puzzle resolution) to listeners without circular dependencies.

### 2.2 Classical AI Algorithm Suite (`AI_Algorithms/`)
- Pure Python implementations of 8 foundational AI paradigms providing both instant evaluation and generator-based step-by-step state yields for visual playback.

### 2.3 Machine Learning Adaptive Pipeline (`ML/`)
- Coordinates unsupervised player clustering, deterministic decision tree difficulty routing, and neural network win probability estimation on every player action.

### 2.4 AI Companion Subsystem (`AI_Agent/`)
- **NovaCompanion (`nova_agent.py`)**: Generates adaptive dialogue, contextual hints, and educational breakdowns.
- **AutonomousSolver (`autonomous_solver.py`)**: Executes verified algorithms directly inside the game environment, automating character actions.
