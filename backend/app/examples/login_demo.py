"""完整执行示例：用户输入“帮我做一个用户登录系统”"""

from pathlib import Path

from app.agent.core import AgentCore
from app.memory.store import MemoryStore
from app.mcp.client import MCPClient, ToolSchema
from app.skills.loader import SkillLoader
from app.tools.filesystem import FileSystemTool
from app.tools.git_tool import GitTool
from app.tools.sandbox import WorkspaceSandbox
from app.tools.shell_tool import ShellTool


BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_ROOT.parent
SKILLS_DIR = BACKEND_ROOT / "skills"


def build_core() -> AgentCore:
    sandbox = WorkspaceSandbox(str(BACKEND_ROOT / "workspace"))
    fs = FileSystemTool(sandbox)
    shell = ShellTool()
    git = GitTool(str(REPO_ROOT))

    mcp = MCPClient()
    mcp.register_tool("filesystem.write", fs.write, lambda: ToolSchema(name="filesystem.write", description="Write file"))
    mcp.register_tool("shell.run", shell.run, lambda: ToolSchema(name="shell.run", description="Run shell command"))
    mcp.register_tool("git.commit", git.commit, lambda: ToolSchema(name="git.commit", description="Commit code"))

    return AgentCore(skill_loader=SkillLoader(str(SKILLS_DIR)), mcp_client=mcp, memory_store=MemoryStore())


def main() -> None:
    task = "帮我做一个用户登录系统"
    core = build_core()

    plan = core.plan(task)
    result = core.execute(task, plan)

    print("Selected skill:", plan.selected_skill)
    print("Plan:", plan.steps)
    print("Tool trace:", result.tool_trace)
    print("Output:", result.output)


if __name__ == "__main__":
    main()
