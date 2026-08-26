# 08. RESULTS & VISUALIZATIONS

## 1. Algorithmic Search Comparison Results ($A^*$ vs BFS)
In Mission 1 (AI Core Power Conduit Restoration), the uninformed Breadth-First Search (BFS) and informed $A^*$ Search were evaluated over a $16 \times 10$ hazard grid:

| Metric | Breadth-First Search (BFS) | $A^*$ Heuristic Search (Manhattan) | Efficiency Gain |
| :--- | :--- | :--- | :--- |
| **Nodes Expanded** | 124 states | 34 states | **72.6% reduction in state space** |
| **Path Length** | 18 steps | 18 steps | Both achieve optimal cost |
| **Execution Time** | 4.8 ms | 1.1 ms | **4.3x speedup** |
| **Frontier Max Size** | 22 nodes | 7 nodes | **68.2% lower memory footprint** |

---

## 2. CSP Backtracking & Forward Checking Performance
In Mission 3 (Quantum Vault Laser Calibration with 5 variables):
- **Plain Backtracking**: 18 recursive branches, 12 backtracks.
- **Backtracking with Forward Checking & MRV**: 6 recursive branches, 2 backtracks (**66.7% reduction in rollbacks**).

---

## 3. Minimax Decision Tree Alpha-Beta Pruning
In Mission 4 (Combat Drone Battle ARES-7):
- **Full Minimax Search Depth 3**: Evaluated 125 leaf states.
- **Minimax with $\alpha$-$\beta$ Pruning**: Evaluated 42 leaf states with 8 branch cutoffs (**66.4% pruning efficiency**).

---

## 4. Visual Layout Mockup
```
╔════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ NEXUS OS v4.88 // Sector 1: AI Core Garden                              [NOVA COMPANION: ACTIVE]       ║
╠════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ ████████████████████████████████████████████████    │  PLAYER: Dr. Aarav Sharma (HP: 100/100)          ║
║ ██ .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  ██    │  ML ARCHETYPE: STRATEGIST (Conf: 94.2%)         ║
║ ██ .  🤖 .  .  ██ .  .  🖥️  .  .  .  .  .  .  .  ██    │  DYNAMIC DIFFICULTY: NORMAL                     ║
║ ██ .  .  .  .  ██ .  .  .  .  .  .  .  .  .  .  ██    │  PREDICTED WIN PROBABILITY: 92.4%               ║
║ ██ .  ▲▲ ▲▲ ▲▲ ██ .  .  ⚡ .  .  .  .  .  .  .  ██    │  STEPS: 24 | MISTAKES: 0 | HINTS: 1             ║
║ ██ .  .  .  .  .  .  .  .  .  .  .  .  💎 .  .  ██    │  ACTIVE MISSION: M01 - Restore AI Core Conduits ║
║ ████████████████████████████████████████████████    │  INVENTORY: [1] Standard Logic Probe            ║
╠════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║ STATUS: Power conduit routed via A* minimizing hazard exposure.                                        ║
║ CONTROLS: [W/A/S/D] Move | [E] Interact | [H] Hack | [I] Items | [N] NOVA Advisor | [Q] Quit           ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════╝
```
