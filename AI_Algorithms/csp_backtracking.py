"""
NEXUS AI REASONING WAR - Constraint Satisfaction Problem (CSP) Solver
Provides Backtracking Search with MRV heuristic, Degree heuristic,
Forward Checking, and live visual rollback logging for Quantum Locks.
"""

from typing import Dict, List, Set, Tuple, Optional, Callable, Any, Generator
import copy


class Variable:
    def __init__(self, name: str, domain: List[Any], label: str = ""):
        self.name = name
        self.domain = list(domain)
        self.label = label or name

    def __repr__(self):
        return f"Var({self.name}, domain_size={len(self.domain)})"


class Constraint:
    """Represents a constraint between one, two, or multiple variables."""
    def __init__(self, scope: List[str], condition: Callable[[Dict[str, Any]], bool], description: str = ""):
        self.scope = scope
        self.condition = condition
        self.description = description

    def is_satisfied(self, assignment: Dict[str, Any]) -> bool:
        # Check if all variables in scope are assigned
        if not all(var in assignment for var in self.scope):
            return True  # Vacuously satisfied until all scope variables assigned
        return self.condition(assignment)


class CSPSolver:
    """
    Backtracking CSP Solver with MRV, Degree Heuristic, Forward Checking,
    and step-by-step generator yielding attempts, failures, and rollbacks.
    """
    def __init__(self, variables: Dict[str, List[Any]], constraints: List[Constraint]):
        self.variables = variables  # var_name -> initial domain
        self.constraints = constraints
        self.backtrack_count = 0
        self.attempt_count = 0

    def is_consistent(self, var: str, value: Any, assignment: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Checks if assigning value to var violates any constraint."""
        local_assignment = dict(assignment)
        local_assignment[var] = value

        for c in self.constraints:
            if var in c.scope:
                if not c.is_satisfied(local_assignment):
                    return False, c.description or f"Violates constraint on {c.scope}"
        return True, None

    def select_unassigned_variable_mrv(self, assignment: Dict[str, Any], domains: Dict[str, List[Any]]) -> str:
        """Selects unassigned variable with Minimum Remaining Values (MRV)."""
        unassigned = [v for v in self.variables if v not in assignment]
        # MRV: sort by smallest domain size
        unassigned.sort(key=lambda v: (len(domains[v]), -self._get_degree(v, assignment)))
        return unassigned[0]

    def _get_degree(self, var: str, assignment: Dict[str, Any]) -> int:
        """Counts constraints involving var and other unassigned variables."""
        degree = 0
        for c in self.constraints:
            if var in c.scope:
                for other in c.scope:
                    if other != var and other not in assignment:
                        degree += 1
        return degree

    def solve(self) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:
        """Instant solve returning solution and statistics."""
        steps = list(self.solve_stepper())
        final_step = steps[-1] if steps else {}
        stats = {
            "attempts": self.attempt_count,
            "backtracks": self.backtrack_count,
            "total_steps": len(steps)
        }
        if final_step.get("status") == "SOLVED":
            return final_step["assignment"], stats
        return None, stats

    def solve_stepper(self) -> Generator[Dict[str, Any], None, None]:
        """
        Step-by-step generator for visual rendering of quantum state alignment,
        displaying tested values, forward checking prunings, and rollbacks.
        """
        self.backtrack_count = 0
        self.attempt_count = 0
        initial_domains = {v: list(dom) for v, dom in self.variables.items()}
        assignment: Dict[str, Any] = {}

        yield {
            "status": "INIT",
            "assignment": dict(assignment),
            "domains": copy.deepcopy(initial_domains),
            "attempts": 0,
            "backtracks": 0,
            "message": f"Initialized CSP Quantum Lock with {len(self.variables)} variables and {len(self.constraints)} constraints."
        }

        yield from self._backtrack_generator(assignment, initial_domains)

    def _backtrack_generator(self, assignment: Dict[str, Any], domains: Dict[str, List[Any]]) -> Generator[Dict[str, Any], None, None]:
        if len(assignment) == len(self.variables):
            yield {
                "status": "SOLVED",
                "assignment": dict(assignment),
                "domains": copy.deepcopy(domains),
                "attempts": self.attempt_count,
                "backtracks": self.backtrack_count,
                "message": f"CSP Solved! Valid harmonic configuration verified: {assignment}."
            }
            return

        var = self.select_unassigned_variable_mrv(assignment, domains)

        for value in list(domains[var]):
            self.attempt_count += 1
            consistent, reason = self.is_consistent(var, value, assignment)

            if consistent:
                assignment[var] = value
                
                # Forward Checking
                new_domains = copy.deepcopy(domains)
                new_domains[var] = [value]
                
                failure = False
                for c in self.constraints:
                    if var in c.scope:
                        for other in c.scope:
                            if other != var and other not in assignment:
                                # Prune invalid values from other's domain
                                valid_other_vals = []
                                for oval in new_domains[other]:
                                    test_assign = dict(assignment)
                                    test_assign[other] = oval
                                    if c.is_satisfied(test_assign):
                                        valid_other_vals.append(oval)
                                new_domains[other] = valid_other_vals
                                if not valid_other_vals:
                                    failure = True
                                    break
                    if failure:
                        break

                yield {
                    "status": "ASSIGN_VALID" if not failure else "FORWARD_CHECK_FAIL",
                    "var": var,
                    "value": value,
                    "assignment": dict(assignment),
                    "domains": copy.deepcopy(new_domains),
                    "attempts": self.attempt_count,
                    "backtracks": self.backtrack_count,
                    "message": f"Assigned {var} = {value}. Forward Checking {'Passed' if not failure else 'Domain Empty for neighbor!'}"
                }

                if not failure:
                    yield from self._backtrack_generator(assignment, new_domains)
                    if len(assignment) == len(self.variables):
                        return  # Solved!

                # Backtrack / Rollback
                del assignment[var]
                self.backtrack_count += 1

                yield {
                    "status": "ROLLBACK",
                    "var": var,
                    "rejected_value": value,
                    "assignment": dict(assignment),
                    "domains": copy.deepcopy(domains),
                    "attempts": self.attempt_count,
                    "backtracks": self.backtrack_count,
                    "message": f"FAILED constraint branch! Rolling back assignment: {var} = {value}. Backtrack #{self.backtrack_count}."
                }
            else:
                self.backtrack_count += 1
                yield {
                    "status": "DIRECT_CONFLICT",
                    "var": var,
                    "rejected_value": value,
                    "reason": reason,
                    "assignment": dict(assignment),
                    "domains": copy.deepcopy(domains),
                    "attempts": self.attempt_count,
                    "backtracks": self.backtrack_count,
                    "message": f"Conflict detected on {var}={value}: {reason}. Attempt rejected."
                }
