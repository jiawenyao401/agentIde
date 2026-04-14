from __future__ import annotations

import re

from app.skills.loader import Skill


class SkillMatcher:
    """轻量语义匹配：支持中文关键词、引号触发词与英文 token。"""

    _split_pattern = re.compile(r"[\s,;，。；、|/()（）:：]+")

    def match(self, task: str, skills: list[Skill]) -> Skill | None:
        lowered_task = task.lower()
        scored: list[tuple[int, Skill]] = []

        for skill in skills:
            score = 0
            keywords = self._extract_keywords(skill)

            for keyword in keywords:
                if not keyword:
                    continue
                if keyword in task or keyword.lower() in lowered_task:
                    score += 3 if len(keyword) >= 4 else 1

            # name 完整命中额外加权
            if skill.name.lower() in lowered_task:
                score += 4

            scored.append((score, skill))

        best_score, best_skill = max(scored, key=lambda x: x[0], default=(0, None))
        return best_skill if best_score > 0 else None

    def _extract_keywords(self, skill: Skill) -> set[str]:
        raw = " ".join([skill.name, skill.description, skill.trigger])

        # 提取中文/英文引号中的短语，如“登录系统”
        quoted = re.findall(r"[\"'“”‘’]([^\"'“”‘’]{2,30})[\"'“”‘’]", raw)

        base_tokens = [token.strip() for token in self._split_pattern.split(raw) if token.strip()]
        keywords = set(base_tokens + quoted)

        # 过滤无意义长句
        return {k for k in keywords if len(k) >= 2}
