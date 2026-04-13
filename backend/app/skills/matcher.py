from __future__ import annotations

from app.skills.loader import Skill


class SkillMatcher:
    """Simple semantic matcher; production可以替换成 embedding 相似度。"""

    def match(self, task: str, skills: list[Skill]) -> Skill | None:
        lowered = task.lower()
        scored: list[tuple[int, Skill]] = []
        for skill in skills:
            score = 0
            for token in {skill.name.lower(), skill.trigger.lower(), skill.description.lower()}:
                if token and token in lowered:
                    score += 2
            for word in skill.description.lower().split():
                if word in lowered:
                    score += 1
            scored.append((score, skill))

        best_score, best_skill = max(scored, key=lambda x: x[0], default=(0, None))
        return best_skill if best_score > 0 else None
