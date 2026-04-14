from pathlib import Path


class WorkspaceSandbox:
    def __init__(self, root: str) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def guard_path(self, relative_path: str) -> Path:
        target = (self.root / relative_path).resolve()
        if not str(target).startswith(str(self.root)):
            raise PermissionError("Path escapes workspace sandbox")
        return target
