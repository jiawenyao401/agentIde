from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

import yaml


@dataclass
class Skill:
    name: str
    description: str
    trigger: str
    root: Path
    markdown: str
    flow: dict
    tools: list[str]


class SkillLoader:
    def __init__(self, skills_dir: str) -> None:
        self.skills_dir = Path(skills_dir)

    def load(self) -> list[Skill]:
        skills: list[Skill] = []
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            flow_yaml = skill_dir / "flow.yaml"
            tools_json = skill_dir / "tools.json"
            if not (skill_md.exists() and flow_yaml.exists() and tools_json.exists()):
                continue

            markdown = skill_md.read_text(encoding="utf-8")
            frontmatter = self._parse_frontmatter(markdown)
            flow = yaml.safe_load(flow_yaml.read_text(encoding="utf-8"))
            tools = json.loads(tools_json.read_text(encoding="utf-8")).get("tools", [])
            skills.append(
                Skill(
                    name=frontmatter.get("name", skill_dir.name),
                    description=frontmatter.get("description", ""),
                    trigger=frontmatter.get("trigger", ""),
                    root=skill_dir,
                    markdown=markdown,
                    flow=flow,
                    tools=tools,
                )
            )
        return skills

    @staticmethod
    def _parse_frontmatter(markdown: str) -> dict:
        parts = markdown.split("---")
        if len(parts) < 3:
            return {}
        return yaml.safe_load(parts[1]) or {}
