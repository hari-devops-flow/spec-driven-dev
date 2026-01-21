import subprocess
import os
from typing import List, Tuple

class GitWrapper:
    """
    Abstractions for Git CLI commands.
    """
    def __init__(self, repo_path: str, dry_run: bool = True):
        self.repo_path = repo_path
        self.dry_run = dry_run

    def _run(self, args: List[str], check: bool = True) -> str:
        cmd = ["git"] + args
        if self.dry_run and args[0] in ["commit", "push", "add"]:
            print(f"[DRY-RUN] Would run: {' '.join(cmd)}")
            return "DRY_RUN_OK"
        
        try:
            result = subprocess.run(
                cmd, 
                cwd=self.repo_path, 
                capture_output=True, 
                text=True, 
                check=check
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # We don't always want to crash (e.g. check if something is a repo)
            if check:
                print(f"[GIT ERROR] Command failed: {' '.join(cmd)}")
                print(f"Stderr: {e.stderr}")
                raise
            return ""

    def status(self) -> str:
        return self._run(["status", "--porcelain", "-b"])

    def diff(self) -> str:
        return self._run(["diff"])
    
    def diff_staged(self) -> str:
        return self._run(["diff", "--cached"])

    def add_all(self):
        self._run(["add", "."])

    def commit(self, message: str):
        self._run(["commit", "-m", message])

    def push(self, branch: str):
        self._run(["push", "origin", branch])
    
    def current_branch(self) -> str:
        return self._run(["rev-parse", "--abbrev-ref", "HEAD"])
    
    def check_remotes(self) -> str:
        return self._run(["remote", "-v"], check=False)
