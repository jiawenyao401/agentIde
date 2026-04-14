from __future__ import annotations

import networkx as nx


class SkillGraph:
    def __init__(self, flow: dict) -> None:
        self.graph = nx.DiGraph()
        for node in flow.get("nodes", []):
            self.graph.add_node(node["id"], **node)
        for edge in flow.get("edges", []):
            self.graph.add_edge(edge["from"], edge["to"])

    def topological_steps(self) -> list[str]:
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("Skill flow must be DAG")
        return list(nx.topological_sort(self.graph))
