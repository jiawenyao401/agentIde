from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.agent.models import AgentPlan
from app.memory.models import MemoryType
from app.memory.store import MemoryStore
from app.mcp.client import MCPClient
from app.observability.logger import get_logger
from app.observability.trace import TraceCollector
from app.skills.executor import SkillExecutor
from app.skills.loader import SkillLoader
from app.skills.matcher import SkillMatcher


@dataclass
class ExecutionResult:
    output: str
    tool_trace: list[dict[str, Any]]


class AgentCore:
    def __init__(self, skill_loader: SkillLoader, mcp_client: MCPClient, memory_store: MemoryStore) -> None:
        self.skill_loader = skill_loader
        self.skill_matcher = SkillMatcher()
        self.skill_executor = SkillExecutor()
        self.mcp_client = mcp_client
        self.memory_store = memory_store
        self.logger = get_logger("agent.core")

    def plan(self, task: str) -> AgentPlan:
        skills = self.skill_loader.load()
        matched_skill = self.skill_matcher.match(task, skills)
        if matched_skill:
            steps = self.skill_executor.run(matched_skill)
            return AgentPlan(steps=steps, selected_skill=matched_skill.name, assigned_agents=self._spawn_agents(steps))

        fallback = ["analyze requirements", "generate code", "write tests", "prepare PR"]
        return AgentPlan(steps=fallback, selected_skill=None, assigned_agents=self._spawn_agents(fallback))

    def route(self, task: str, plan: AgentPlan) -> dict[str, str]:
        routes = {}
        for step in plan.steps:
            if "test" in step:
                routes[step] = "shell.run"
            elif "pr" in step or "commit" in step:
                routes[step] = "git.commit"
            else:
                routes[step] = "filesystem.write"
        self.logger.info("routes selected: %s", routes)
        return routes

    def execute(self, task: str, plan: AgentPlan) -> ExecutionResult:
        trace = TraceCollector()
        routes = self.route(task, plan)
        tool_trace: list[dict[str, Any]] = []

        with trace.span("execution", {"steps": len(plan.steps)}):
            for step in plan.steps:
                tool_name = routes[step]
                payload = self._build_payload(task, step, tool_name)
                result = self.mcp_client.call_tool(tool_name, payload)
                tool_trace.append({"step": step, "tool": tool_name, "payload": payload, "result": str(result)[:200]})

        self.memory_store.add(MemoryType.episodic, f"Task: {task} | Plan: {plan.steps}")
        self.memory_store.add(MemoryType.semantic, f"Completed task pattern: {task}")

        return ExecutionResult(
            output=f"Executed {len(plan.steps)} steps with {len(tool_trace)} tool calls.",
            tool_trace=tool_trace + [
                {"trace": event.name, "duration_ms": round(event.duration_ms, 2), "metadata": event.metadata}
                for event in trace.events
            ],
        )

    @staticmethod
    def _spawn_agents(steps: list[str]) -> list[str]:
        return [f"agent-{idx+1}:{step}" for idx, step in enumerate(steps)]

    @staticmethod
    def _build_payload(task: str, step: str, tool_name: str) -> dict[str, Any]:
        if tool_name == "filesystem.write":
            filename = step.replace(" ", "_") + ".md"
            return {"path": f"artifacts/{filename}", "content": f"# Step\n{step}\n\nTask:{task}\n"}
        if tool_name == "shell.run":
            return {"command": "echo running tests"}
        if tool_name == "git.commit":
            return {"message": f"chore: {step}"}
        return {}
