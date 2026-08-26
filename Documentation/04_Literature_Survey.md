# 04. LITERATURE SURVEY

## 1. Classical Heuristic Search in Spatial Navigation
Heuristic graph search algorithms, pioneered by Hart, Nilsson, and Raphael (1968) with $A^*$, represent the cornerstone of pathfinding in computational environments. An admissible heuristic $h(n) \le h^*(n)$ guarantees optimality while pruning unpromising branches of the search graph (Russell & Norvig, 2020). In video game environments (*Portal*, *The Legend of Zelda*), search algorithms are often hidden behind navigation meshes. Visualizing $f(n) = g(n) + h(n)$ step-by-step transforms pathfinding into an active learning tool where users observe how heuristic weights guide search frontiers away from hazards.

---

## 2. Constraint Satisfaction and Heuristic Backtracking
Constraint Satisfaction Problems (CSP) formalize problems where states are defined by variables $X_i$ within domains $D_i$ satisfying constraints $C_j$ (Dechter, 2003). Classical backtracking search suffers from exponential worst-case time complexity $O(d^n)$. To mitigate thrashing, modern solvers employ variable ordering heuristics such as the Minimum Remaining Values (MRV) heuristic ("fail-first principle") and Degree heuristic, combined with Forward Checking for domain reduction (Kumar, 1992). Applying CSP to laser frequency alignment and cryptographic locks allows players to visualize constraint propagation and rollbacks in a physical narrative context.

---

## 3. Knowledge Representation and Forward Chaining Deduction
Rule-based expert systems (Shortliffe, 1976; Forgy, 1982) employ forward chaining algorithms to derive logical theorems from verified atomic facts using Horn clauses ($P_1 \land P_2 \implies Q$). In forensic investigation games (*Ace Attorney*), establishing contradictions between testimonies and physical timestamps mirrors forward chaining deduction graphs, demonstrating the mechanics of automated inference.

---

## 4. Adversarial Search & Alpha-Beta Pruning
Adversarial decision theory in zero-sum deterministic games traces back to Von Neumann's Minimax Theorem (1928) and Knuth & Moore's (1975) analysis of $\alpha$-$\beta$ pruning. Pruning allows algorithms to evaluate deeper game trees by eliminating sub-trees that cannot influence the final decision. Implementing this within a turn-based tactical combat drone battle grounds abstract minimax evaluation values in gameplay choices.

---

## 5. Machine Learning in Player Telemetry & Adaptive Difficulty
Dynamic Difficulty Adjustment (DDA) (Hunicke, 2005) and player profiling using unsupervised clustering (Drachen et al., 2009) utilize live telemetry to dynamically scale game parameters. Unsupervised K-Means clustering segments players based on behavioral traits, while interpretable Decision Trees (Quinlan, 1986) provide deterministic rule paths for parameter modulation. Artificial Neural Networks (Haykin, 1998) model multi-variate non-linear interactions to predict task completion probabilities.
