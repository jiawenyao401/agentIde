from __future__ import annotations

from app.skills.graph import SkillGraph
from app.skills.loader import Skill


class SkillExecutor:
    def run(self, skill: Skill) -> list[str]:
        graph = SkillGraph(skill.flow)
        return graph.topological_steps()
