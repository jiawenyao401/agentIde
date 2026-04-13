from pathlib import Path

from git import InvalidGitRepositoryError, Repo


class GitTool:
    def __init__(self, repo_path: str) -> None:
        resolved = Path(repo_path).resolve()
        try:
            # 支持在子目录启动（例如在 backend/ 内执行 uvicorn）。
            self.repo = Repo(resolved, search_parent_directories=True)
        except InvalidGitRepositoryError:
            self.repo = None

    def commit(self, message: str) -> str:
        if self.repo is None:
            return "git_unavailable"

        self.repo.git.add(A=True)
        if not self.repo.is_dirty(untracked_files=True):
            return "no_changes"
        commit = self.repo.index.commit(message)
        return commit.hexsha

    def create_pr_payload(self, title: str, body: str) -> dict:
        return {"title": title, "body": body}
