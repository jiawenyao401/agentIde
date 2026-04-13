from pathlib import Path

from git import Repo


class GitTool:
    def __init__(self, repo_path: str) -> None:
        self.repo = Repo(Path(repo_path).resolve())

    def commit(self, message: str) -> str:
        self.repo.git.add(A=True)
        if not self.repo.is_dirty(untracked_files=True):
            return "no_changes"
        commit = self.repo.index.commit(message)
        return commit.hexsha

    def create_pr_payload(self, title: str, body: str) -> dict:
        return {"title": title, "body": body}
