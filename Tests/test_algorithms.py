"""
Unit Tests - NEXUS AI Algorithm Suite
Tests A*, BFS, CSP Backtracking, Forward Chaining, Minimax, MEU, STRIPS, and Min-Cut.
"""

import unittest
from AI_Algorithms.astar import AStarSearch
from AI_Algorithms.bfs import BreadthFirstSearch
from AI_Algorithms.csp_backtracking import CSPSolver, Constraint
from AI_Algorithms.forward_chaining import ForwardChainingEngine, Fact, Rule
from AI_Algorithms.minimax import MinimaxEngine, GameState, CombatAction
from AI_Algorithms.decision_theory import DecisionTheoryEngine, DecisionOption, Outcome
from AI_Algorithms.strips_planner import STRIPSPlanner, Action, State
from AI_Algorithms.graph_algorithms import GraphEngine


class TestAIAlgorithms(unittest.TestCase):
    def test_astar_search_optimality(self):
        grid = [[0 for _ in range(10)] for _ in range(10)]
        # Add a wall at column 5
        def is_walkable(pos):
            x, y = pos
            if not (0 <= x < 10 and 0 <= y < 10):
                return False
            if x == 5 and y < 8:
                return False
            return True

        astar = AStarSearch(heuristic_type="manhattan")
        path, stats = astar.find_path(grid, (1, 1), (8, 1), is_walkable)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (1, 1))
        self.assertEqual(path[-1], (8, 1))
        self.assertGreater(stats["expanded_nodes"], 0)

    def test_bfs_vs_astar_expansion(self):
        grid = [[0 for _ in range(10)] for _ in range(10)]
        start, goal = (0, 0), (9, 9)
        astar = AStarSearch()
        bfs = BreadthFirstSearch()
        _, astar_stats = astar.find_path(grid, start, goal)
        _, bfs_stats = bfs.find_path(grid, start, goal)
        # A* expands fewer or equal nodes than uninformed BFS
        self.assertLessEqual(astar_stats["expanded_nodes"], bfs_stats["expanded_nodes"])

    def test_csp_backtracking_solver(self):
        variables = {"A": [1, 2, 3], "B": [1, 2, 3], "C": [1, 2, 3]}
        constraints = [
            Constraint(["A", "B"], lambda a: a["A"] != a["B"], "A != B"),
            Constraint(["B", "C"], lambda a: a["B"] != a["C"], "B != C"),
            Constraint(["A", "C"], lambda a: a["A"] + a["C"] == 4, "A + C == 4")
        ]
        solver = CSPSolver(variables, constraints)
        sol, stats = solver.solve()
        self.assertIsNotNone(sol)
        self.assertNotEqual(sol["A"], sol["B"])
        self.assertNotEqual(sol["B"], sol["C"])
        self.assertEqual(sol["A"] + sol["C"], 4)

    def test_forward_chaining_inference(self):
        engine = ForwardChainingEngine(
            initial_facts=[Fact("A"), Fact("B")],
            rules=[
                Rule("R1", ["A", "B"], "C"),
                Rule("R2", ["C"], "D")
            ]
        )
        deduced = engine.infer()
        self.assertIn("C", deduced)
        self.assertIn("D", deduced)

    def test_minimax_combat_decision(self):
        engine = MinimaxEngine(max_depth=3)
        state = GameState(ai_hp=50, ai_energy=100, player_hp=10, player_energy=0, is_ai_turn=True)
        best_act, val, stats = engine.select_best_action(state, is_ai=True)
        # Should pick attack to finish off 10hp player
        self.assertIn(best_act, [CombatAction.ATTACK, CombatAction.OVERCLOCK])

    def test_decision_theory_meu(self):
        opt1 = DecisionOption("A1", "Option 1", "", [Outcome("O1", 1.0, {"val": 100})], {"val": 1.0})
        opt2 = DecisionOption("A2", "Option 2", "", [Outcome("O2", 1.0, {"val": 40})], {"val": 1.0})
        engine = DecisionTheoryEngine([opt1, opt2])
        evals = engine.evaluate_all_options()
        self.assertEqual(evals[0]["action_id"], "A1")
        self.assertEqual(evals[0]["meu"], 100.0)

    def test_strips_planning(self):
        init = State({"door_locked", "has_key"})
        goal = {"door_open"}
        actions = [
            Action("unlock", preconditions={"door_locked", "has_key"},
                   add_effects={"door_open"}, delete_effects={"door_locked"})
        ]
        planner = STRIPSPlanner(init, goal, actions)
        plan, stats = planner.plan()
        self.assertIsNotNone(plan)
        self.assertEqual(len(plan), 1)
        self.assertEqual(plan[0].name, "unlock")

    def test_graph_min_cut_quarantine(self):
        ge = GraphEngine()
        ge.add_node("S", "Source", is_infected=True)
        ge.add_node("A", "Node A")
        ge.add_node("T", "Sink", is_critical=True)
        ge.add_edge("S", "A", capacity=5.0, bidirectional=False)
        ge.add_edge("A", "T", capacity=5.0, bidirectional=False)

        cuts, flow, stats = ge.compute_min_cut_quarantine("S", "T")
        self.assertEqual(flow, 5.0)
        self.assertGreaterEqual(len(cuts), 1)


if __name__ == "__main__":
    unittest.main()
