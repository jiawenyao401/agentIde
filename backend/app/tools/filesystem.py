from app.tools.sandbox import WorkspaceSandbox


class FileSystemTool:
    def __init__(self, sandbox: WorkspaceSandbox) -> None:
        self.sandbox = sandbox

    def read(self, path: str) -> str:
        target = self.sandbox.guard_path(path)
        return target.read_text(encoding="utf-8")

    def write(self, path: str, content: str) -> str:
        target = self.sandbox.guard_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"wrote:{path}"
