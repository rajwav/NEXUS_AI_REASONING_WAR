"""
NEXUS AI REASONING WAR - Forward Chaining Inference Engine
Provides knowledge representation, Horn clause deduction, and interactive
graph tracing for Digital Forensics and Evidence Analysis.
"""

from typing import Dict, List, Set, Tuple, Optional, Any, Generator
import copy


class Fact:
    def __init__(self, name: str, source: str = "OBSERVATION", confidence: float = 1.0, description: str = ""):
        self.name = name
        self.source = source
        self.confidence = confidence
        self.description = description or name

    def __eq__(self, other):
        if isinstance(other, Fact):
            return self.name == other.name
        return self.name == str(other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Fact({self.name})"


class Rule:
    """Production Rule: IF all premises are true, THEN deduce conclusion."""
    def __init__(self, rule_id: str, premises: List[str], conclusion: str, explanation: str = ""):
        self.rule_id = rule_id
        self.premises = set(premises)
        self.conclusion = conclusion
        self.explanation = explanation

    def is_triggered(self, known_facts: Set[str]) -> bool:
        return self.premises.issubset(known_facts)


class ForwardChainingEngine:
    """
    Forward chaining inference engine with step-by-step derivation history
    and knowledge graph construction for forensic investigations.
    """
    def __init__(self, initial_facts: Optional[List[Fact]] = None, rules: Optional[List[Rule]] = None):
        self.facts: Dict[str, Fact] = {}
        if initial_facts:
            for f in initial_facts:
                self.facts[f.name] = f
        self.rules: List[Rule] = list(rules) if rules else []
        self.inference_tree: List[Dict[str, Any]] = []

    def add_fact(self, fact: Fact):
        self.facts[fact.name] = fact

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def infer(self) -> Set[str]:
        """Instant deduction returning all derived facts."""
        steps = list(self.infer_stepper())
        return set(self.facts.keys())

    def infer_stepper(self) -> Generator[Dict[str, Any], None, None]:
        """
        Step-by-step generator for real-time visual knowledge graph construction.
        """
        known_fact_names = set(self.facts.keys())
        fired_rules: Set[str] = set()
        step_number = 0

        yield {
            "status": "INIT",
            "step": 0,
            "known_facts": list(known_fact_names),
            "new_fact": None,
            "rule_fired": None,
            "message": f"Initialized Knowledge Base with {len(known_fact_names)} base facts and {len(self.rules)} rules."
        }

        while True:
            new_deduction_made = False

            for rule in self.rules:
                if rule.rule_id in fired_rules:
                    continue

                if rule.is_triggered(known_fact_names):
                    if rule.conclusion not in known_fact_names:
                        step_number += 1
                        fired_rules.add(rule.rule_id)
                        new_fact = Fact(rule.conclusion, source=f"INFERRED_BY_{rule.rule_id}", description=rule.explanation)
                        self.facts[new_fact.name] = new_fact
                        known_fact_names.add(new_fact.name)
                        new_deduction_made = True

                        inference_step = {
                            "step": step_number,
                            "rule_id": rule.rule_id,
                            "premises": list(rule.premises),
                            "conclusion": rule.conclusion,
                            "explanation": rule.explanation
                        }
                        self.inference_tree.append(inference_step)

                        yield {
                            "status": "RULE_FIRED",
                            "step": step_number,
                            "known_facts": list(known_fact_names),
                            "new_fact": new_fact.name,
                            "rule_fired": rule.rule_id,
                            "premises": list(rule.premises),
                            "explanation": rule.explanation,
                            "message": f"Rule [{rule.rule_id}] FIRED! Premises {list(rule.premises)} => Deduces: [{rule.conclusion}]."
                        }
                        break  # restart rule evaluation loop

            if not new_deduction_made:
                break

        yield {
            "status": "COMPLETE",
            "step": step_number,
            "known_facts": list(known_fact_names),
            "fired_rules_count": len(fired_rules),
            "total_facts": len(known_fact_names),
            "message": f"Inference complete. {len(fired_rules)} logical rules executed, establishing truth consensus."
        }
