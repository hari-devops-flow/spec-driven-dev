from datetime import datetime
from typing import Dict, Optional

from .config import Config, RepoConfig
from .safety import SafetyGuard
from .state import StateManager
from .git_ops import GitWrapper

class GitAutoCommitterAgent:
    def __init__(self, config: Config, dry_run: bool, force_run: bool = False):
        self.config = config
        self.dry_run = dry_run
        self.force_run = force_run
        
        self.guard = SafetyGuard(config)
        self.state_manager = StateManager()

    def generate_message(self, status: str, repo_config: RepoConfig) -> str:
        """
        Simple deterministic commit message generator.
        """
        prefix = repo_config.commit_prefix
        lines = status.splitlines()
        
        # Simple heuristic analysis
        # Porcelain status format: ' XY PATH'
        modified = [l for l in lines if "M " in l or " M" in l]
        added = [l for l in lines if "??" in l]
        deleted = [l for l in lines if "D " in l or " D" in l]
        
        details = []
        if modified:
            details.append(f"modified {len(modified)} files")
        if added:
            details.append(f"added {len(added)} files")
        if deleted:
            details.append(f"deleted {len(deleted)} files")
            
        if not details:
            msg_body = "minor updates"
        else:
            msg_body = ", ".join(details)
            
        return f"{prefix} {msg_body} ({datetime.now().strftime('%Y-%m-%d')})"

    def run_repo(self, repo_config: RepoConfig):
        print(f"\n--- Checking Repo: {repo_config.path} ---")
        
        # 1. Safety Check
        if not self.guard.validate_repo(repo_config.path):
            return

        # 2. State Check (Idempotency)
        if not self.force_run and not self.state_manager.should_run(repo_config.path):
            print(f"[SKIP] Agent already ran for {repo_config.path} today.")
            return

        git = GitWrapper(repo_config.path, self.dry_run)

        # 3. Observe
        try:
            current_branch = git.current_branch()
            status = git.status()
        except Exception as e:
            print(f"[ERROR] Failed to read git status: {e}")
            return
            
        print(f"[OBSERVE] Branch: {current_branch}")
        
        # Branch validation
        if repo_config.branch and current_branch != repo_config.branch:
            print(f"[SKIP] Current branch '{current_branch}' does not match configured '{repo_config.branch}'.")
            return

        # 4. Decide Strategy
        is_clean = False
        # If status only has 1 line and it starts with ##, it's just branch info -> Clean
        lines = status.splitlines()
        if len(lines) == 0:
             is_clean = True
        elif len(lines) == 1 and lines[0].startswith("##"):
             is_clean = True
             
        if is_clean:
             print("[DECIDE] Repo is clean. No action needed.")
             return

        print("[DECIDE] Changes detected. Planning commit.")

        # 5. Plan & Act
        commit_msg = self.generate_message(status, repo_config)
        print(f"[PLAN] Message: {commit_msg}")
        
        git.add_all()
        git.commit(commit_msg)
        
        # 6. Push (Optional)
        # Global auto_push setting or per-repo setting? 
        # Config schema has per-repo 'auto_push'.
        push_needed = repo_config.auto_push
        
        if push_needed:
             print(f"[ACT] Pushing to origin/{current_branch}...")
             git.push(current_branch)
        else:
             print("[ACT] Auto-push disabled. Skipping push.")

        # 7. Record State
        if not self.dry_run:
            self.state_manager.record_run(
                repo_config.path, 
                "commit_push" if push_needed else "commit", 
                "success",
                commit_msg
            )

    def run(self):
        print(f"=== Git Agent Starting (DryRun={self.dry_run}, Force={self.force_run}) ===")
        for repo in self.config.repositories:
            self.run_repo(repo)
        print("=== Git Agent Finished ===")
