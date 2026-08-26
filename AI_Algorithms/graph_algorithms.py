"""
NEXUS AI REASONING WAR - Graph Algorithms & Min-Cut Firewall Engine
Provides Dijkstra Shortest Path, Breadth-First Flow, and Min-Cut algorithms
to isolate spreading malware in the Network Control Center.
"""

from typing import Dict, List, Set, Tuple, Optional, Any, Generator
from collections import deque
import heapq
import math


class NetworkNode:
    def __init__(self, node_id: str, name: str, is_infected: bool = False, is_critical: bool = False):
        self.node_id = node_id
        self.name = name
        self.is_infected = is_infected
        self.is_critical = is_critical


class GraphEngine:
    """Handles network graph representation, Dijkstra, and Min-Cut quarantine calculations."""
    def __init__(self):
        self.nodes: Dict[str, NetworkNode] = {}
        self.edges: Dict[str, Dict[str, float]] = {}  # u -> {v: weight/capacity}

    def add_node(self, node_id: str, name: str, is_infected: bool = False, is_critical: bool = False):
        self.nodes[node_id] = NetworkNode(node_id, name, is_infected, is_critical)
        if node_id not in self.edges:
            self.edges[node_id] = {}

    def add_edge(self, u: str, v: str, capacity: float = 1.0, bidirectional: bool = True):
        if u not in self.edges:
            self.edges[u] = {}
        if v not in self.edges:
            self.edges[v] = {}
        self.edges[u][v] = capacity
        if bidirectional:
            self.edges[v][u] = capacity

    def dijkstra_shortest_path(self, source: str, target: str) -> Tuple[Optional[List[str]], float]:
        distances: Dict[str, float] = {n: math.inf for n in self.nodes}
        distances[source] = 0.0
        previous: Dict[str, Optional[str]] = {n: None for n in self.nodes}
        pq = [(0.0, source)]

        while pq:
            curr_dist, u = heapq.heappop(pq)
            if curr_dist > distances[u]:
                continue
            if u == target:
                break

            for v, weight in self.edges.get(u, {}).items():
                alt = curr_dist + weight
                if alt < distances[v]:
                    distances[v] = alt
                    previous[v] = u
                    heapq.heappush(pq, (alt, v))

        if distances[target] == math.inf:
            return None, math.inf

        path = []
        curr = target
        while curr:
            path.append(curr)
            curr = previous[curr]
        path.reverse()
        return path, distances[target]

    def compute_min_cut_quarantine(self, source: str, sink: str) -> Tuple[List[Tuple[str, str]], float, Dict[str, Any]]:
        """
        Uses Edmonds-Karp / Ford-Fulkerson to find maximum flow and minimum cut
        to isolate the source malware node from reaching the sink critical server.
        """
        # Build residual capacity graph
        residual: Dict[str, Dict[str, float]] = {n: {} for n in self.nodes}
        for u in self.nodes:
            for v in self.nodes:
                residual[u][v] = 0.0

        for u in self.edges:
            for v, cap in self.edges[u].items():
                residual[u][v] = cap

        def bfs_find_path() -> Optional[Tuple[List[str], float]]:
            parent: Dict[str, Optional[str]] = {source: None}
            visited: Set[str] = {source}
            queue = deque([source])

            while queue:
                u = queue.popleft()
                if u == sink:
                    # Found augmenting path
                    path = []
                    curr = sink
                    while curr:
                        path.append(curr)
                        curr = parent[curr]
                    path.reverse()
                    
                    # Find bottleneck capacity
                    bottleneck = min(residual[path[i]][path[i+1]] for i in range(len(path)-1))
                    return path, bottleneck

                for v, cap in residual.get(u, {}).items():
                    if v not in visited and cap > 1e-6:
                        visited.add(v)
                        parent[v] = u
                        queue.append(v)
            return None

        max_flow = 0.0
        while True:
            result = bfs_find_path()
            if not result:
                break
            aug_path, flow_val = result
            max_flow += flow_val
            for i in range(len(aug_path) - 1):
                u, v = aug_path[i], aug_path[i+1]
                residual[u][v] -= flow_val
                residual[v][u] += flow_val

        # Find reachable vertices from source in residual graph (S component)
        reachable: Set[str] = set()
        q = deque([source])
        reachable.add(source)
        while q:
            u = q.popleft()
            for v, cap in residual.get(u, {}).items():
                if v not in reachable and cap > 1e-6:
                    reachable.add(v)
                    q.append(v)

        # Min cut edges: edges in original graph from S to T (unreachable)
        min_cut_edges: List[Tuple[str, str]] = []
        for u in reachable:
            for v in self.edges.get(u, {}):
                if v not in reachable and self.edges[u][v] > 0:
                    min_cut_edges.append((u, v))

        stats = {
            "max_flow_quarantine_capacity": max_flow,
            "isolated_source_cluster": list(reachable),
            "protected_sink_cluster": [n for n in self.nodes if n not in reachable],
            "recommended_firewall_cuts": min_cut_edges
        }
        return min_cut_edges, max_flow, stats
