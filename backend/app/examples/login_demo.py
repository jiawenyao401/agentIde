"""完整执行示例：用户输入“帮我做一个用户登录系统”"""

from app.agent.core import AgentCore
from app.memory.store import MemoryStore
from app.mcp.client import MCPClient, ToolSchema
from app.skills.loader import SkillLoader
from app.tools.filesystem import FileSystemTool
from app.tools.git_tool import GitTool
from app.tools.sandbox import WorkspaceSandbox
from app.tools.shell_tool import ShellTool


def build_core() -> AgentCore:
    sandbox = WorkspaceSandbox("./workspace")
    fs = FileSystemTool(sandbox)
    shell = ShellTool()
    git = GitTool(".")

    mcp = MCPClient()
    mcp.register_tool("filesystem.write", fs.write, lambda: ToolSchema(name="filesystem.write", description="Write file"))
    mcp.register_tool("shell.run", shell.run, lambda: ToolSchema(name="shell.run", description="Run shell command"))
    mcp.register_tool("git.commit", git.commit, lambda: ToolSchema(name="git.commit", description="Commit code"))

    return AgentCore(skill_loader=SkillLoader("backend/skills"), mcp_client=mcp, memory_store=MemoryStore())


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
