"""
NEXUS AI REASONING WAR - AI Explainability Data Models
Defines structured data classes and type definitions for AI reasoning traces,
search trees, decision nodes, and theoretical principles.
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
import json


@dataclass
class TreeNode:
    """Represents a node in the hierarchical AI Search Tree."""
    id: str
    label: str
    action: str
    status: str  # 'ACCEPTED', 'REJECTED', 'PRUNED', 'BACKTRACK', 'ROOT', 'GOAL'
    state_summary: Optional[str] = None
    heuristic_score: Optional[Union[int, float, str]] = None
    cost_g: Optional[Union[int, float]] = None
    cost_h: Optional[Union[int, float]] = None
    cost_f: Optional[Union[int, float]] = None
    constraints_passed: Optional[Dict[str, bool]] = None
    reason: Optional[str] = None
    children: List['TreeNode'] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "action": self.action,
            "status": self.status,
            "state_summary": self.state_summary,
            "heuristic_score": self.heuristic_score,
            "cost_g": self.cost_g,
            "cost_h": self.cost_h,
            "cost_f": self.cost_f,
            "constraints_passed": self.constraints_passed,
            "reason": self.reason,
            "children": [c.to_dict() for c in self.children]
        }


@dataclass
class TimelineStep:
    """Represents a discrete chronological decision step in the AI solving sequence."""
    step_index: int
    type: str  # 'ASSIGN', 'MOVE', 'ROTATE', 'REVEAL', 'FLAG', 'BACKTRACK', 'PRUNE'
    selected_target: str
    candidates_domain: List[Any]
    chosen_value: Any
    rejected_alternatives: List[Any]
    constraint_checks: Dict[str, str]
    decision_outcome: str  # 'ACCEPTED', 'REJECTED', 'BACKTRACK', 'OPTIMAL'
    rationale: str
    theory_principle: str
    state_snapshot: Optional[Dict[str, Any]] = None
    tree_node_ref: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_index": self.step_index,
            "type": self.type,
            "selected_target": self.selected_target,
            "candidates_domain": self.candidates_domain,
            "chosen_value": self.chosen_value,
            "rejected_alternatives": self.rejected_alternatives,
            "constraint_checks": self.constraint_checks,
            "decision_outcome": self.decision_outcome,
            "rationale": self.rationale,
            "theory_principle": self.theory_principle,
            "state_snapshot": self.state_snapshot,
            "tree_node_ref": self.tree_node_ref
        }


@dataclass
class ExplanationSession:
    """Complete serialized payload for frontend explainability visualizations."""
    game_id: str
    algorithm: str
    complexity_class: str
    theory_overview: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    timeline: List[TimelineStep] = field(default_factory=list)
    search_tree: Optional[TreeNode] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "game_id": self.game_id,
            "algorithm": self.algorithm,
            "complexity_class": self.complexity_class,
            "theory_overview": self.theory_overview,
            "metrics": self.metrics,
            "timeline": [step.to_dict() for step in self.timeline],
            "search_tree": self.search_tree.to_dict() if self.search_tree else None
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
