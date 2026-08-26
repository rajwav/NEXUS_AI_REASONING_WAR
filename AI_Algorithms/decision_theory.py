"""
NEXUS AI REASONING WAR - Decision Theory & Expected Utility Engine
Solves multi-attribute ethical dilemmas by calculating Maximum Expected Utility (MEU):
U(Action) = Sum(P(Outcome|Action) * Utility(Outcome)) across competing objectives.
"""

from typing import Dict, List, Tuple, Optional, Any, Generator


class Outcome:
    def __init__(self, name: str, probability: float,
                 utilities: Dict[str, float], description: str = ""):
        self.name = name
        self.probability = probability
        self.utilities = utilities  # attribute_name -> score (-100 to +100)
        self.description = description


class DecisionOption:
    def __init__(self, action_id: str, name: str, description: str,
                 outcomes: List[Outcome], ethical_weight_profile: Dict[str, float]):
        self.action_id = action_id
        self.name = name
        self.description = description
        self.outcomes = outcomes
        self.weights = ethical_weight_profile  # e.g., {"human_safety": 0.5, "data_preservation": 0.3, "power_conservation": 0.2}

    def calculate_expected_utility(self) -> Tuple[float, Dict[str, float]]:
        """
        Calculates total MEU and per-attribute expected values.
        """
        attribute_expected: Dict[str, float] = {attr: 0.0 for attr in self.weights}
        total_utility = 0.0

        for outcome in self.outcomes:
            for attr, weight in self.weights.items():
                attr_val = outcome.utilities.get(attr, 0.0)
                expected_part = outcome.probability * attr_val
                attribute_expected[attr] += expected_part
                total_utility += expected_part * weight

        return round(total_utility, 3), {k: round(v, 3) for k, v in attribute_expected.items()}


class DecisionTheoryEngine:
    """Calculates optimal actions under risk, uncertainty, and ethical constraints."""
    def __init__(self, options: List[DecisionOption]):
        self.options = options

    def evaluate_all_options(self) -> List[Dict[str, Any]]:
        results = []
        for opt in self.options:
            meu, breakdown = opt.calculate_expected_utility()
            results.append({
                "action_id": opt.action_id,
                "name": opt.name,
                "description": opt.description,
                "meu": meu,
                "breakdown": breakdown,
                "outcomes": [
                    {
                        "name": o.name,
                        "probability": o.probability,
                        "utilities": o.utilities,
                        "desc": o.description
                    } for o in opt.outcomes
                ]
            })
        results.sort(key=lambda r: r["meu"], reverse=True)
        return results

    def solve_stepper(self) -> Generator[Dict[str, Any], None, None]:
        results = []
        yield {
            "status": "START",
            "message": f"Analyzing {len(self.options)} strategic ethical choices using Maximum Expected Utility (MEU)."
        }

        for opt in self.options:
            meu, breakdown = opt.calculate_expected_utility()
            entry = {
                "action_id": opt.action_id,
                "name": opt.name,
                "meu": meu,
                "breakdown": breakdown
            }
            results.append(entry)
            yield {
                "status": "OPTION_EVALUATED",
                "option": entry,
                "message": f"Evaluated [{opt.name}] -> MEU Score: {meu} | Breakdown: {breakdown}"
            }

        results.sort(key=lambda r: r["meu"], reverse=True)
        best = results[0]

        yield {
            "status": "OPTIMAL_DECISION",
            "best_option": best,
            "all_options": results,
            "message": f"Optimal decision under ethical constraints: [{best['name']}] with MEU {best['meu']}."
        }
