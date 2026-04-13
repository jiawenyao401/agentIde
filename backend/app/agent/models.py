from dataclasses import dataclass, field


@dataclass
class AgentPlan:
    steps: list[str]
    selected_skill: str | None = None
    assigned_agents: list[str] = field(default_factory=list)
