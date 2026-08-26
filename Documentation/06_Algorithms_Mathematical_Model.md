# 06. ALGORITHMS & MATHEMATICAL MODELS

This document specifies the exact mathematical formulations implemented across the AI and Machine Learning engines in **NEXUS AI REASONING WAR**.

---

## 1. Heuristic Pathfinding ($A^*$ Search)
The evaluation function for a node $n$ on a 2D grid is defined as:
$$f(n) = g(n) + h(n)$$

Where:
- $g(n)$ is the exact cost from the start node to $n$.
- $h(n)$ is the admissible Manhattan heuristic to goal node $(x_g, y_g)$:
$$h(n) = |x_n - x_g| + |y_n - y_g|$$

Since movement is restricted to four orthogonal directions (North, South, East, West) with uniform step cost $c=1$, $h(n)$ satisfies admissibility:
$$\forall n, \quad h(n) \le h^*(n)$$
and monotonicity (consistency):
$$h(n) \le c(n, a, n') + h(n')$$

---

## 2. Constraint Satisfaction Problem (CSP)
A CSP is defined by a triple $\langle X, D, C \rangle$:
- Variables $X = \{X_1, X_2, \dots, X_m\}$
- Domains $D = \{D_1, D_2, \dots, D_m\}$
- Constraints $C = \{C_1, C_2, \dots, C_k\}$

The solver implements **Minimum Remaining Values (MRV)** heuristic for variable selection:
$$X_{\text{MRV}} = \arg\min_{X_i \in X_{\text{unassigned}}} |D_i|$$
with Degree heuristic breaking ties by maximizing constraints with remaining unassigned variables. **Forward Checking** prunes domain values:
$$D_j \leftarrow D_j \setminus \{v \in D_j \mid \exists c \in C \text{ violating } \langle X_i=v_i, X_j=v \rangle\}$$

---

## 3. Game-Theoretic Minimax with $\alpha$-$\beta$ Pruning
For game state $s$, the minimax value is computed recursively:
$$\text{Minimax}(s) = \begin{cases} 
\text{Utility}(s) & \text{if Terminal}(s) \\
\max_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a)) & \text{if Player is MAX} \\
\min_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a)) & \text{if Player is MIN}
\end{cases}$$

Alpha-beta bounds maintain:
- $\alpha$: Highest utility found so far along the path for MAX.
- $\beta$: Lowest utility found so far along the path for MIN.

A sub-tree is pruned whenever:
$$\alpha \ge \beta$$

---

## 4. Maximum Expected Utility (MEU)
For an action $a$ with non-deterministic outcomes $s'$, the expected utility is:
$$EU(a) = \sum_{s'} P(s' \mid a) \cdot U(s')$$
where multi-attribute utility is decomposed as:
$$U(s') = w_1 \cdot U_{\text{safety}}(s') + w_2 \cdot U_{\text{data}}(s') + w_3 \cdot U_{\text{power}}(s')$$
with $\sum w_i = 1.0$. The optimal policy is:
$$a^* = \arg\max_{a} EU(a)$$

---

## 5. K-Means Clustering for Player Archetyping
Given $N$ telemetry vectors $\mathbf{x}_i \in \mathbb{R}^5$ (velocity, error rate, hint dependency, risk score, autonomy), K-Means minimizes inertia:
$$J = \sum_{j=1}^{k} \sum_{\mathbf{x}_i \in S_j} \|\mathbf{x}_i - \boldsymbol{\mu}_j\|^2$$
Centroid updates follow:
$$\boldsymbol{\mu}_j = \frac{1}{|S_j|} \sum_{\mathbf{x}_i \in S_j} \mathbf{x}_i$$

---

## 6. Artificial Neural Network (ANN) Success Predictor
The architecture consists of a Multi-Layer Perceptron (MLP) ($5 \to 8 \to 1$):
- Hidden Layer Activation: $\mathbf{h} = \text{ReLU}(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1) = \max(0, \mathbf{W}_1 \mathbf{x} + \mathbf{b}_1)$
- Output Layer Activation: $\hat{y} = \sigma(\mathbf{W}_2 \mathbf{h} + b_2) = \frac{1}{1 + e^{-(\mathbf{W}_2 \mathbf{h} + b_2)}}$
- Loss Function: Binary Cross-Entropy Loss:
$$\mathcal{L} = -\frac{1}{N}\sum_{i=1}^N \left[ y_i \log(\hat{y}_i) + (1-y_i) \log(1 - \hat{y}_i) \right]$$
