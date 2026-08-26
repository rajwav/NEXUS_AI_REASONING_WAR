"""
NEXUS AI REASONING WAR - Reasoning Tracer
Formats live algorithm execution streams into clear, high-tech visual trace blocks.
"""

from typing import Dict, List, Any, Optional


class ReasoningTracer:
    """Formats live algorithm execution steps for terminal, GUI, and web renderers."""
    def __init__(self):
        self.trace_history: List[Dict[str, Any]] = []

    def log_step(self, step_info: Dict[str, Any]):
        self.trace_history.append(step_info)

    def render_last_trace_block(self) -> str:
        if not self.trace_history:
            return "[NO ACTIVE ALGORITHM TRACE - SYSTEM IDLE]"

        last = self.trace_history[-1]
        msg = last.get("message", "")
        status = last.get("status", "RUNNING")
        lines = [
            f"┌─── [AI REASONING TRACE] ────────────────────────────────────────┐",
            f"│ STATUS : {status:<55}│",
            f"│ DETAIL : {msg[:55]:<55}│"
        ]

        if "current_node" in last:
            node = last["current_node"]
            node_info = f"Pos: ({node.get('x')},{node.get('y')}) | g={node.get('g')} h={node.get('h')} f(n)={node.get('f')}"
            lines.append(f"│ NODE   : {node_info:<55}│")

        if "var" in last and "value" in last:
            csp_info = f"Var: {last.get('var')} = {last.get('value')} | Backtracks: {last.get('backtracks', 0)}"
            lines.append(f"│ CSP    : {csp_info:<55}│")

        if "rule_fired" in last:
            rule_info = f"Rule: {last.get('rule_fired')} -> {last.get('new_fact')}"
            lines.append(f"│ LOGIC  : {rule_info:<55}│")

        lines.append(f"└─────────────────────────────────────────────────────────────────┘")
        return "\n".join(lines)
