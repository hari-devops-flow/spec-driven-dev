import os
import sys
import yaml
import subprocess
import argparse
from datetime import datetime
from typing import List, Dict, Optional

# ==========================================
# 0. Infrastructure & Tool Abstraction
# ==========================================

class GitWrapper:
    """
    Abstractions for Git CLI commands.
    """
    def __init__(self, repo_path: str, dry_run: bool = True):
        self.repo_path = repo_path
        self.dry_run = dry_run

    def _run(self, args: List[str], check: bool = True) -> str:
        cmd = ["git"] + args
        if self.dry_run and args[0] in ["commit", "push"]:
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
            print(f"[GIT ERROR] Command failed: {' '.join(cmd)}")
            print(f"Stderr: {e.stderr}")
            if check:
                raise
            return ""

    def status(self) -> str:
        return self._run(["status", "--porcelain", "-b"])

    def diff(self) -> str:
        return self._run(["diff"])

    def add_all(self):
        self._run(["add", "."])

    def commit(self, message: str):
        self._run(["commit", "-m", message])

    def push(self, branch: str):
        self._run(["push", "origin", branch])
    
    def current_branch(self) -> str:
        return self._run(["rev-parse", "--abbrev-ref", "HEAD"])

class SafetyGuard:
    """
    Enforces security boundaries defined in the Spec.
    """
    def __init__(self, config: Dict):
        self.allowed_paths = [os.path.abspath(p) for p in config.get("allowed_paths", [])]
        self.allowed_branches = config.get("branch_allowlist", ["main"])

    def validate_repo(self, path: str) -> bool:
        abs_path = os.path.abspath(path)
        # Check if path is in allowlist
        if not any(abs_path.startswith(allowed) for allowed in self.allowed_paths):
            print(f"[SECURITY] REJECTED: Repo {abs_path} is NOT in allowed_paths.")
            return False
        
        # Check if it is a git repo
        if not os.path.isdir(os.path.join(abs_path, ".git")):
            print(f"[SECURITY] REJECTED: {abs_path} is not a git repository.")
            return False
            
        return True

    def validate_branch(self, branch: str) -> bool:
        if branch not in self.allowed_branches:
            print(f"[SECURITY] REJECTED: Branch '{branch}' is not in allowlist.")
            return False
        return True

# ==========================================
# 1. The Agent Logic (Control Loop)
# ==========================================

class GitAutoCommitterAgent:
    def __init__(self, config: Dict, repo_path: str, dry_run: bool):
        self.config = config
        self.repo_path = repo_path
        self.dry_run = dry_run
        
        self.git = GitWrapper(repo_path, dry_run)
        self.guard = SafetyGuard(config)

    def generate_message(self, status: str, diff: str) -> str:
        """
        In a real agent, this calls an LLM.
        For Phase 2, we use a deterministic heuristic or 'Mock LLM'.
        """
        prefix = self.config.get("commit_prefix", "[Auto]")
        lines = status.splitlines()
        
        # Simple heuristic analysis
        modified = [l for l in lines if l.startswith(" M")]
        added = [l for l in lines if l.startswith("??")]
        
        details = []
        if modified:
            details.append(f"modified {len(modified)} files")
        if added:
            details.append(f"added {len(added)} files")
            
        msg_body = ", ".join(details)
        return f"{prefix} Update: {msg_body} ({datetime.now().strftime('%Y-%m-%d')})"

    def run(self):
        print(f"--- Agent Starting: {self.repo_path} (DryRun={self.dry_run}) ---")

        # Step 0: Security Check
        if not self.guard.validate_repo(self.repo_path):
            return

        # Step 1: Observe
        try:
            status = self.git.status()
            current_branch = self.git.current_branch()
        except Exception as e:
            print(f"[FATAL] Could not read git status: {e}")
            return

        print(f"[OBSERVE] Branch: {current_branch}")
        
        if not self.guard.validate_branch(current_branch):
            return

        # Step 2: Decide Strategy
        if "clean" in status and "working tree clean" in status: # Basic check, porcelain format differs
            # Porcelain -b output:
            # ## main...origin/main
            # (nothing else if clean)
            if len(status.splitlines()) <= 1: 
                print("[DECIDE] Repo is clean. No action needed.")
                return

        print("[DECIDE] Changes detected. Planning commit.")
        
        # Step 3: Plan (Generate Message)
        # Note: We simulate 'git add .' behavior by looking at status
        diff = self.git.diff() # Only unstaged by default, but good enough for mock
        commit_msg = self.generate_message(status, diff)
        print(f"[PLAN] Commit Message: '{commit_msg}'")

        # Step 4: Act (Execute)
        self.git.add_all()
        self.git.commit(commit_msg)
        
        # Step 5: Push
        print(f"[ACT] Pushing to origin/{current_branch}...")
        self.git.push(current_branch)
        
        print("--- Agent Finished Successfully ---")

# ==========================================
# 2. Entrypoint
# ==========================================

def load_config(path: str) -> Dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Git Auto-Committer Agent")
    parser.add_argument("--repo", required=True, help="Path to the repository")
    parser.add_argument("--config", default="git-agent.config.yaml", help="Path to config file")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without changes")
    parser.add_argument("--force-run", action="store_true", help="Actual execution (disables default safe mode)") # Extra safety
    
    args = parser.parse_args()
    
    # Logic: Default to dry_run unless force-run is present (inverted logic for safety if user forgets flags)
    # Actually, standard is: flag enables the mode. 
    # Let's stick to: --dry-run enables dry run. ABSENCE of --dry-run means REAL RUN?
    # Spec says: "dry_run default: true".
    # So we should enforce dry_run IS true, unless a specific flag disables it.
    
    is_dry_run = True
    if args.force_run:
        is_dry_run = False
    if args.dry_run:
        is_dry_run = True # explicit flag wins
        
    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"Config file not found: {args.config}")
        sys.exit(1)

    agent = GitAutoCommitterAgent(config, args.repo, is_dry_run)
    agent.run()

if __name__ == "__main__":
    main()
