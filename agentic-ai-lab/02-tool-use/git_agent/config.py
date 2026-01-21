import yaml
import os
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class RepoConfig:
    path: str
    branch: str = "main"
    commit_prefix: str = "[SDD-Agent]"
    auto_push: bool = False

@dataclass
class GlobalSettings:
    dry_run_default: bool = True
    max_commits_per_run: int = 1
    log_file: str = "git-agent.log"

class Config:
    def __init__(self, data: Dict):
        self.version = data.get("version", 1)
        self.repositories: List[RepoConfig] = []
        self.settings = GlobalSettings()
        
        self._load_repos(data.get("repositories", []))
        self._load_settings(data.get("settings", {}))

    def _load_repos(self, repos_data: List[Dict]):
        for r in repos_data:
            path = r.get("path")
            if not path:
                continue # Skip invalid config
            
            self.repositories.append(RepoConfig(
                path=os.path.abspath(path),
                branch=r.get("branch", "main"),
                commit_prefix=r.get("commit_prefix", "[SDD-Agent]"),
                auto_push=r.get("auto_push", False)
            ))

    def _load_settings(self, settings_data: Dict):
        self.settings.dry_run_default = settings_data.get("dry_run_default", True)
        self.settings.max_commits_per_run = settings_data.get("max_commits_per_run", 1)
        self.settings.log_file = settings_data.get("log_file", "git-agent.log")

def load_config(path: str) -> Config:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
        
    return Config(data)
