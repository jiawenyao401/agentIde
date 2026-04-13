import subprocess


class ShellTool:
    def run(self, command: str) -> str:
        proc = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return proc.stdout if proc.returncode == 0 else proc.stderr
