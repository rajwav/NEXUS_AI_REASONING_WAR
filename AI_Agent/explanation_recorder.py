"""
NEXUS AI REASONING WAR - Generic AI Explanation Recorder
Provides a unified recorder for all 5 puzzle solvers to capture decision steps,
search tree topologies, alternative rejections, constraints, and algorithmic theories.
"""

from typing import Dict, List, Any, Optional, Union
from AI_Agent.explanation_models import TreeNode, TimelineStep, ExplanationSession


class ExplanationRecorder:
    """
    Standardized explanation recorder that connects AI Solvers to the Explainability UI.
    Builds both chronological step-by-step timelines and hierarchical search trees.
    """

    def __init__(self, game_id: str = "generic", algorithm: str = "Search",
                 complexity_class: str = "O(b^d)", theory_overview: str = "",
                 root_label: str = "START", root_state_summary: str = ""):
        self.game_id = game_id
        self.algorithm = algorithm
        self.complexity_class = complexity_class
        self.theory_overview = theory_overview
        
        # Root of search tree
        self.root_node = TreeNode(
            id="root",
            label=root_label,
            action="START",
            status="ROOT",
            state_summary=root_state_summary,
            reason="Initial problem state initialized."
        )
        self.nodes_by_id: Dict[str, TreeNode] = {"root": self.root_node}
        self.timeline: List[TimelineStep] = []
        self.metrics: Dict[str, Any] = {}

    def start_session(self, game_id: str, algorithm: str, complexity_class: str,
                      theory_overview: str, root_label: str = "START", root_state_summary: str = ""):
        """Initializes or resets an explainability recording session."""
        self.game_id = game_id
        self.algorithm = algorithm
        self.complexity_class = complexity_class
        self.theory_overview = theory_overview
        self.root_node = TreeNode(
            id="root",
            label=root_label,
            action="START",
            status="ROOT",
            state_summary=root_state_summary,
            reason="Initial problem state initialized."
        )
        self.nodes_by_id = {"root": self.root_node}
        self.timeline.clear()
        self.metrics.clear()

    def add_tree_node(self, node_id: str, parent_id: Optional[str] = "root",
                      label: str = "", action: str = "", status: str = "ACCEPTED",
                      state_summary: Optional[str] = None,
                      heuristic_score: Optional[Union[int, float, str]] = None,
                      cost_g: Optional[Union[int, float]] = None,
                      cost_h: Optional[Union[int, float]] = None,
                      cost_f: Optional[Union[int, float]] = None,
                      constraints_passed: Optional[Dict[str, bool]] = None,
                      reason: Optional[str] = None) -> TreeNode:
        """Adds a branch/decision node into the hierarchical search tree."""
        node = TreeNode(
            id=node_id,
            label=label or action,
            action=action,
            status=status,
            state_summary=state_summary,
            heuristic_score=heuristic_score,
            cost_g=cost_g,
            cost_h=cost_h,
            cost_f=cost_f,
            constraints_passed=constraints_passed,
            reason=reason
        )
        self.nodes_by_id[node_id] = node

        # Link to parent if available
        pid = parent_id if parent_id and parent_id in self.nodes_by_id else "root"
        self.nodes_by_id[pid].children.append(node)
        return node

    def add_decision(self, step_index: int, type: str, selected_target: str,
                     candidates_domain: List[Any], chosen_value: Any,
                     rejected_alternatives: List[Any],
                     constraint_checks: Dict[str, str],
                     decision_outcome: str, rationale: str,
                     theory_principle: str,
                     state_snapshot: Optional[Dict[str, Any]] = None,
                     tree_node_ref: Optional[str] = None) -> TimelineStep:
        """Appends a chronological decision event into the timeline."""
        step = TimelineStep(
            step_index=step_index,
            type=type,
            selected_target=selected_target,
            candidates_domain=candidates_domain,
            chosen_value=chosen_value,
            rejected_alternatives=rejected_alternatives,
            constraint_checks=constraint_checks,
            decision_outcome=decision_outcome,
            rationale=rationale,
            theory_principle=theory_principle,
            state_snapshot=state_snapshot,
            tree_node_ref=tree_node_ref
        )
        self.timeline.append(step)
        return step

    def add_metric(self, key: str, value: Any):
        """Records a solver profiling or performance metric."""
        self.metrics[key] = value

    def finish_session(self) -> Dict[str, Any]:
        """Finalizes and returns the complete serializable explanation payload."""
        session = ExplanationSession(
            game_id=self.game_id,
            algorithm=self.algorithm,
            complexity_class=self.complexity_class,
            theory_overview=self.theory_overview,
            metrics=self.metrics,
            timeline=self.timeline,
            search_tree=self.root_node
        )
        return session.to_dict()
