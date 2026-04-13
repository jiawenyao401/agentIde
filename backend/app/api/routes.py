from __future__ import annotations

from fastapi import APIRouter

from app.agent.core import AgentCore
from app.memory.store import MemoryStore
from app.mcp.client import MCPClient, ToolSchema
from app.schemas import TaskRequest, TaskResponse
from app.skills.loader import SkillLoader
from app.tools.browser_tool import BrowserTool
from app.tools.filesystem import FileSystemTool
from app.tools.git_tool import GitTool
from app.tools.sandbox import WorkspaceSandbox
from app.tools.shell_tool import ShellTool

router = APIRouter(prefix="/api")

sandbox = WorkspaceSandbox("./workspace")
filesystem = FileSystemTool(sandbox)
shell_tool = ShellTool()
git_tool = GitTool(".")
browser_tool = BrowserTool()

mcp_client = MCPClient()
mcp_client.register_tool("filesystem.write", filesystem.write, lambda: ToolSchema(name="filesystem.write", description="Write file"))
mcp_client.register_tool("shell.run", shell_tool.run, lambda: ToolSchema(name="shell.run", description="Run shell command"))
mcp_client.register_tool("git.commit", git_tool.commit, lambda: ToolSchema(name="git.commit", description="Commit repository"))
mcp_client.register_tool("browser.fetch", browser_tool.fetch, lambda: ToolSchema(name="browser.fetch", description="Fetch webpage"))

core = AgentCore(skill_loader=SkillLoader("backend/skills"), mcp_client=mcp_client, memory_store=MemoryStore())


@router.post("/run", response_model=TaskResponse)
def run_task(req: TaskRequest) -> TaskResponse:
    plan = core.plan(req.prompt)
    result = core.execute(req.prompt, plan)
    return TaskResponse(plan=plan.steps, selected_skill=plan.selected_skill, tool_trace=result.tool_trace, output=result.output)


@router.get("/tools")
def list_tools() -> list[dict]:
    return [schema.__dict__ for schema in mcp_client.list_tools()]
